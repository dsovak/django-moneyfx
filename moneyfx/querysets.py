from django.db.models import QuerySet

from moneyfx import conf


class ExchangeRateQuerySet(QuerySet):
    def get_rates(self, date, source):
        return self.filter(source=source, created_date__lte=date).latest()

    def get_rate(self, currency, date, source):
        supported_sources = [sources[1] for sources in conf.EXCHANGE_RATES_SOURCES]

        if source not in supported_sources:
            raise KeyError('FX source is not supported.')

        currency = ('c_%s' % currency).lower()
        exchange_rates = self.latest() if date is None else self.get_rates(date, source)

        return getattr(exchange_rates, currency)