# Cron job logic for updating exchange rates will be here.

import requests
import xml.etree.ElementTree as ET
from datetime import date

from . import conf
from .models import ExchangeRate


def save_actual_exchange_rates_from_ecb():
    save_exchange_rates()


def save_exchange_rates():
    url_ecb = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    response = requests.get(url=url_ecb)
    namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    rates = {}
    today = date.today()
    tree = ET.fromstring(response.text)

    if response.status_code != 200:
        print(f'ECB fetch failed: {response.status_code}')
        return

    date_ecb_str = tree.find('.//ex:Cube[@time]', namespaces=namespaces).get('time')
    for cube in tree.findall('.//ex:Cube[@currency]', namespaces=namespaces):
        currency = cube.attrib['currency']
        rate = cube.attrib['rate']
        rate = round(float(rate), 4)
        rates['c_' + currency.lower()] = rate

    rates['validity_date'] = today
    rates['created_date'] = date_ecb_str
    # Save or update ExchangeRate
    obj, created = ExchangeRate.objects.get_or_create(validity_date=today, source=conf.SOURCE_ECB, defaults=rates)
    if not created:
        for k, v in rates.items():
            setattr(obj, k, v)
        obj.save()
