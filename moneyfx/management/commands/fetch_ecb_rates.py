from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from collections import defaultdict
import xml.etree.ElementTree as ET
from typing import Optional

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from moneyfx.models import ExchangeRate

# Official ECB historical XML (1999 -> latest)
DEFAULT_ECB_XML = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml"
ECB_NS = {"ex": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}


class Command(BaseCommand):
    help = (
        "Fetch historical Euro FX reference rates from the ECB historical XML and "
        "import/update them into ExchangeRate from a chosen date (default 2023-01-01) to today."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--from-date",
            dest="from_date",
            type=str,
            default="2023-01-01",
            help="Import rates from this date (inclusive). Format: YYYY-MM-DD. Default: 2023-01-01",
        )
        parser.add_argument(
            "--to-date",
            dest="to_date",
            type=str,
            default=None,
            help="Import rates up to this date (inclusive). Format: YYYY-MM-DD. Default: today",
        )
        parser.add_argument(
            "--url",
            dest="url",
            type=str,
            default=DEFAULT_ECB_XML,
            help="Override the ECB historical XML URL if needed.",
        )

    def handle(self, *args, **options):
        start = self._parse_date(options.get("from_date") or "2023-01-01")
        end = self._parse_date(options.get("to_date")) if options.get("to_date") else date.today()
        url = options.get("url") or DEFAULT_ECB_XML

        # Determine allowed currency fields from model to avoid unknown fields
        allowed_rate_fields = {
            f.name for f in ExchangeRate._meta.get_fields() if f.name.startswith("c_") and not f.name.endswith("_amount")
        }

        self.stdout.write(self.style.NOTICE(f"Downloading ECB XML from: {url}"))
        resp = requests.get(url, timeout=90)
        resp.raise_for_status()

        root = ET.fromstring(resp.content)

        # Map of date -> { c_usd: Decimal(...), ... }
        by_date: dict[date, dict] = defaultdict(dict)

        # Iterate through each date cube
        for time_cube in root.findall('.//ex:Cube[@time]', namespaces=ECB_NS):
            time_str = time_cube.attrib.get("time")
            if not time_str:
                continue
            try:
                dt = datetime.strptime(time_str, "%Y-%m-%d").date()
            except ValueError:
                continue

            if dt < start or dt > end:
                continue

            # Iterate currencies for this date
            for cube in time_cube.findall('ex:Cube[@currency]', namespaces=ECB_NS):
                code = cube.attrib.get("currency", "").strip().upper()
                rate_str = cube.attrib.get("rate")
                if not code or not rate_str:
                    continue

                field_name = f"c_{code.lower()}"
                if field_name not in allowed_rate_fields:
                    # Skip currencies we don't model
                    continue

                try:
                    rate = Decimal(rate_str)
                except (InvalidOperation, ValueError):
                    continue

                # ECB quotes 1 EUR = rate * <currency>, so _amount stays default 1
                by_date[dt][field_name] = rate

        created, updated = 0, 0
        source = getattr(settings, "SOURCE_ECB", "ECB")

        for validity_date, fields in sorted(by_date.items()):
            defaults = {
                "created_date": validity_date,
                "fixed_base_currency": True,
                "source": source,
            }
            defaults.update(fields)

            _, was_created = ExchangeRate.objects.update_or_create(
                validity_date=validity_date, source=source, defaults=defaults
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Imported range {start} -> {end}. ExchangeRate created: {created}, updated: {updated}."
            )
        )

    @staticmethod
    def _parse_date(value: Optional[str]) -> date:
        if not value:
            return date.today()
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception as exc:
            raise RuntimeError(f"Invalid date '{value}'. Use YYYY-MM-DD.") from exc
