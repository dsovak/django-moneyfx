from django.db import models
from django.utils.translation import gettext_lazy as _

from moneyfx import conf
from moneyfx.querysets import ExchangeRateQuerySet


class ExchangeRate(models.Model):
    validity_date = models.DateField(_('validity date'))
    created_date = models.DateField(_('created date'))
    c_eur = models.DecimalField('EUR', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_czk = models.DecimalField('CZK', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_pln = models.DecimalField('PLN', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_huf = models.DecimalField('HUF', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_huf_amount = models.PositiveIntegerField(_('HUF amount'), default=1)
    c_usd = models.DecimalField('USD', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_jpy = models.DecimalField('JPY', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_jpy_amount = models.PositiveIntegerField(_('JPY amount'), default=1)
    c_bgn = models.DecimalField('BGN', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_dkk = models.DecimalField('DKK', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_gbp = models.DecimalField('GBP', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_ron = models.DecimalField('RON', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_sek = models.DecimalField('SEK', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_chf = models.DecimalField('CHF', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_isk = models.DecimalField('ISK', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_isk_amount = models.PositiveIntegerField(_('ISK amount'), default=1)
    c_nok = models.DecimalField('NOK', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_hrk = models.DecimalField('HRK', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_try = models.DecimalField('TRY', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_aud = models.DecimalField('AUD', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_brl = models.DecimalField('BRL', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_cad = models.DecimalField('CAD', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_cny = models.DecimalField('CNY', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_hkd = models.DecimalField('HKD', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_idr = models.DecimalField('IDR', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_idr_amount = models.PositiveIntegerField(_('IDR amount'), default=1)
    c_ils = models.DecimalField('ILS', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_inr = models.DecimalField('INR', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_inr_amount = models.PositiveIntegerField(_('INR amount'), default=1)
    c_krw = models.DecimalField('KRW', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_krw_amount = models.PositiveIntegerField(_('KRW amount'), default=1)
    c_mxn = models.DecimalField('MXN', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_myr = models.DecimalField('MYR', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_nzd = models.DecimalField('NZD', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_php = models.DecimalField('PHP', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_php_amount = models.PositiveIntegerField(_('PHP amount'), default=1)
    c_sgd = models.DecimalField('SGD', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_thb = models.DecimalField('THB', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    c_thb_amount = models.PositiveIntegerField(_('THB amount'), default=1)
    c_zar = models.DecimalField('ZAR', max_digits=10, decimal_places=4, blank=True, null=True, default=None)
    fixed_base_currency = models.BooleanField(_('customer'), default=True)
    source = models.CharField(_('source'), choices=conf.EXCHANGE_RATES_SOURCES, max_length=10, default=conf.SOURCE_ECB)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    objects = ExchangeRateQuerySet.as_manager()

    class Meta:
        verbose_name = _('Exchange Rate')
        verbose_name_plural = _('Exchange Rates')

        get_latest_by = 'validity_date'
        unique_together = ('validity_date', 'source')

    def __str__(self):
        return f"ExchangeRate({self.validity_date}, {self.source})"

    def get_currency_amount(self, currency):
        currency_amount_name = f'c_{currency}_amount'.lower()
        return getattr(self, currency_amount_name, 1)
