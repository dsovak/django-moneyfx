import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'moneyfx.tests.settings'
django.setup()

from moneyfx.services import CurrencyExchangeService
from decimal import Decimal
from unittest import TestCase
from djmoney.money import Money


class TestCurrencyConverterService(TestCase):
    def setUp(self):
        self.converter_service = CurrencyExchangeService()
        self.source_CNB = 'CNB'
        self.source_ECB = 'ECB'
        self.source_NBP = 'NBP'
        self.rates_CNB = self.get_czech_CNB_rates()
        self.rates_ECB = self.get_euro_ECB_rates()
        self.rates_NBP = self.get_euro_NBP_rates()

    # EURO ECB source
    def test_ECB_source_CZK_to_EUR(self):
        converted_money = self.convert(25, 'CZK', 'EUR', self.rates_ECB, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'EUR1.06')

    def test_ECB_source_EUR_to_CZK(self):
        converted_money = self.convert(10, 'EUR', 'CZK', self.rates_ECB, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'CZK236.58')

    def test_ECB_source_HUF_to_EUR(self):
        converted_money = self.convert(400, 'HUF', 'EUR', self.rates_ECB, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'EUR1.04')

    def test_ECB_source_EUR_to_HUF(self):
        converted_money = self.convert(10, 'EUR', 'HUF', self.rates_ECB, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'HUF3847.50')

    def test_ECB_source_RON_to_EUR(self):
        converted_money = self.convert(25, 'RON', 'EUR', self.rates_ECB, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'EUR5.08')

    def test_ECB_source_EUR_to_RON(self):
        converted_money = self.convert(10, 'EUR', 'RON', self.rates_ECB, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'RON49.23')

    # CZECH CNB source
    def test_CNB_source_EUR_to_CZK(self):
        converted_money = self.convert(10, 'EUR', 'CZK', self.rates_CNB, self.source_CNB)
        self.assert_money(self.money_to_str(converted_money), 'CZK236.60')

    def test_CNB_source_CZK_to_EUR(self):
        converted_money = self.convert(25, 'CZK', 'EUR', self.rates_CNB, self.source_CNB)
        self.assert_money(self.money_to_str(converted_money), 'EUR1.06')

    def test_CNB_source_PLN_to_CZK(self):
        converted_money = self.convert(10, 'PLN', 'CZK', self.rates_CNB, self.source_CNB)
        self.assert_money(self.money_to_str(converted_money), 'CZK50.48')

    def test_CNB_source_CZK_to_PLN(self):
        converted_money = self.convert(25, 'CZK', 'PLN', self.rates_CNB, self.source_CNB)
        self.assert_money(self.money_to_str(converted_money), 'PLN4.95')

    # POLAND NBP source
    def test_NBP_source_EUR_to_PLN(self):
        converted_money = self.convert(10, 'EUR', 'PLN', self.rates_NBP, self.source_NBP)
        self.assert_money(self.money_to_str(converted_money), 'PLN45.68')

    def test_NBP_source_PLN_to_EUR(self):
        converted_money = self.convert(45, 'PLN', 'EUR', self.rates_NBP, self.source_NBP)
        self.assert_money(self.money_to_str(converted_money), 'EUR9.85')

    def test_NBP_source_CZK_to_PLN(self):
        converted_money = self.convert(30, 'CZK', 'PLN', self.rates_NBP, self.source_NBP)
        self.assert_money(self.money_to_str(converted_money), 'PLN5.86')

    def test_NBP_source_PLN_to_CZK(self):
        converted_money = self.convert(10, 'PLN', 'CZK', self.rates_NBP, self.source_NBP)
        self.assert_money(self.money_to_str(converted_money), 'CZK51.18')

    # Helper methods
    def convert(self, amount, currency_from, currency_to, rates, source):
        money = Money(amount, currency_from)
        return self.converter_service.convert_money(money, currency_to, rates=rates, source=source)

    def money_to_str(self, money):
        return f"{money.currency.code}{money.amount.quantize(Decimal('1.00'))}"

    def assert_money(self, actual, expected):
        self.assertEqual(actual, expected)

    def get_czech_CNB_rates(self):
        # Simulate ExchangeRate for CNB
        class Rates:
            source = 'CNB'
            fixed_base_currency = False
            c_eur = Decimal('23.660')
            c_pln = Decimal('5.048')
            c_ron = Decimal('4.806')
            c_huf = Decimal('6.144')
            c_huf_amount = 100
            def get_currency_amount(self, currency):
                return 1
        return Rates()

    def get_euro_ECB_rates(self):
        # Simulate ExchangeRate for ECB
        class Rates:
            source = 'ECB'
            fixed_base_currency = True
            c_eur = Decimal('1')
            c_czk = Decimal('23.658')
            c_huf = Decimal('384.75')
            c_ron = Decimal('4.923')
            def get_currency_amount(self, currency):
                return 1
        return Rates()

    def get_euro_NBP_rates(self):
        # Simulate ExchangeRate for NBP
        class Rates:
            source = 'NBP'
            fixed_base_currency = False
            c_eur = Decimal('4.5683')
            c_huf = Decimal('1.2281')
            c_czk = Decimal('0.1954')
            c_pln = Decimal('1')
            c_huf_amount = 100
            def get_currency_amount(self, currency):
                return 1
        return Rates()
