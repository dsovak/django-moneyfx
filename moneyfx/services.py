from datetime import datetime
from django.core.cache import cache
from decimal import Decimal
from djmoney.money import Money

from moneyfx import conf
from moneyfx.models import ExchangeRate


class CurrencyExchangeService:
    def get_rates(self, date, source=conf.SOURCE_ECB):
        if date is None:
            cache_key_rates = 'exchange_rates'
        cache_key_version = str(date) + '_' + str(source)
        cached_rates = cache.get(cache_key_rates, version=cache_key_version)
        if cached_rates:
            rates = cached_rates
        else:
            rates = ExchangeRate.objects.filter(validity_date=date, source=source).first()
            cache.set(cache_key_rates, rates, timeout=2592000, version=cache_key_version)
        return rates

    def get_rate(self, rates, currency):
        currency = ('c_%s' % currency).lower()
        return getattr(rates, currency)

    def convert_money(self, money, currency_to, date=None, rates=None, rate=None, source=conf.SOURCE_ECB):
        if money is None:
            return None
        currency_from = money.currency.code
        if currency_from.upper() == currency_to.upper():
            return money
        if money.amount == 0:
            return Money(0, currency_to)
        if rates:
            source = rates.source
        else:
            date = date if date else datetime.now().date()
            rates = self.get_rates(date, source)
        base_source_currency = self.get_source_currency(source)
        # direct conversion
        if base_source_currency in [currency_from, currency_to]:
            currency_for_rate = currency_from if currency_from != base_source_currency else currency_to
            rate = self.get_rate(rates, currency_for_rate) if not rate else rate
            rate = rate / rates.get_currency_amount(currency_for_rate)
            # rate from base source currency
            if currency_from == base_source_currency:
                if not rates.fixed_base_currency:
                    rate = (1 / rate)
            # rate to base source currency
            elif currency_to == base_source_currency:
                if rates.fixed_base_currency:
                    rate = (1 / rate)
            amount = Decimal(money.amount) * Decimal(rate)
            return Money(amount, currency_to)
        # indirect conversion (via base currency)
        else:
            money_base = self.convert_money(money, base_source_currency, date, rates, None, source)
            return self.convert_money(money_base, currency_to, date, rates, None, source)

    def get_source_currency(self, rate_source):
        currency_sources = conf.CURRENCY_RATE_SOURCES
        return list(currency_sources.keys())[list(conf.CURRENCY_RATE_SOURCES.values()).index(rate_source)] \
            if rate_source else None
