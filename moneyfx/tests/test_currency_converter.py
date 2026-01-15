import os
import django
from datetime import date

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
            validity_date = date(2025, 12, 31)
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
            c_bgn = Decimal('1.95583')
            c_hrk = Decimal('7.5345')
            validity_date = date(2021, 12, 31)
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
            validity_date = date(2025, 12, 31)
            def get_currency_amount(self, currency):
                return 1
        return Rates()

    # EUROZONE REPLACEMENT TESTS - BGN (Bulgaria adopted EUR on 2026-01-01)
    def test_ECB_source_BGN_to_EUR_after_replacement(self):
        """BGN should be treated as EUR (1:1) after 2026-01-01"""
        rates = self.get_euro_ECB_rates_after_bgn_replacement()
        converted_money = self.convert(1000, 'BGN', 'EUR', rates, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'EUR1000.00')

    def test_ECB_source_BGN_to_EUR_before_replacement(self):
        """BGN should use historical rate before 2026-01-01"""
        converted_money = self.convert(1000, 'BGN', 'EUR', self.rates_ECB, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'EUR511.29')

    def test_ECB_source_EUR_to_BGN_after_replacement(self):
        """EUR to BGN should be 1:1 after 2026-01-01"""
        rates = self.get_euro_ECB_rates_after_bgn_replacement()
        converted_money = self.convert(1000, 'EUR', 'BGN', rates, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'BGN1000.00')

    def test_ECB_source_BGN_to_CZK_after_replacement(self):
        """BGN to CZK after replacement: BGN treated as EUR, then converted to CZK"""
        rates = self.get_euro_ECB_rates_after_bgn_replacement()
        converted_money = self.convert(100, 'BGN', 'CZK', rates, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'CZK2365.80')

    def test_ECB_source_CZK_to_BGN_after_replacement(self):
        """CZK to BGN after replacement: CZK to EUR, then EUR treated as BGN"""
        rates = self.get_euro_ECB_rates_after_bgn_replacement()
        converted_money = self.convert(2365.80, 'CZK', 'BGN', rates, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'BGN100.00')

    def test_ECB_source_BGN_to_BGN_after_replacement(self):
        """BGN to BGN after replacement should return same amount"""
        rates = self.get_euro_ECB_rates_after_bgn_replacement()
        converted_money = self.convert(1000, 'BGN', 'BGN', rates, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'BGN1000.00')

    # EUROZONE REPLACEMENT TESTS - HRK (Croatia adopted EUR on 2023-01-01)
    def test_ECB_source_HRK_to_EUR_after_replacement(self):
        """HRK should be treated as EUR (1:1) after 2023-01-01"""
        rates = self.get_euro_ECB_rates_after_hrk_replacement()
        converted_money = self.convert(1000, 'HRK', 'EUR', rates, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'EUR1000.00')

    def test_ECB_source_HRK_to_EUR_before_replacement(self):
        """HRK should use historical rate before 2023-01-01"""
        converted_money = self.convert(1000, 'HRK', 'EUR', self.rates_ECB, self.source_ECB)
        self.assert_money(self.money_to_str(converted_money), 'EUR132.72')

    # Helper methods for eurozone replacement rates
    def get_euro_ECB_rates_after_bgn_replacement(self):
        """ECB rates after BGN replacement (2026-01-01 or later)"""
        class Rates:
            source = 'ECB'
            fixed_base_currency = True
            c_eur = Decimal('1')
            c_czk = Decimal('23.658')
            c_huf = Decimal('384.75')
            c_ron = Decimal('4.923')
            # BGN rate is None after replacement
            c_bgn = None
            validity_date = date(2026, 1, 1)
            def get_currency_amount(self, currency):
                return 1
        return Rates()


    def get_euro_ECB_rates_after_hrk_replacement(self):
        class Rates:
            source = 'ECB'
            fixed_base_currency = True
            c_eur = Decimal('1')
            c_czk = Decimal('23.658')
            c_huf = Decimal('384.75')
            c_ron = Decimal('4.923')
            c_hrk = None
            validity_date = date(2023, 1, 1)
            def get_currency_amount(self, currency):
                return 1
        return Rates()

