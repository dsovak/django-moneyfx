from django.conf import settings as django_settings
from . import settings as default_settings

DEBUG = getattr(django_settings, 'DEBUG', default_settings.DEBUG)

CURRENCY_EUR = getattr(django_settings, 'MULTICURRENCY_CURRENCY_EUR', default_settings.CURRENCY_EUR)
CURRENCY_CZK = getattr(django_settings, 'MULTICURRENCY_CZK', default_settings.CURRENCY_CZK)
CURRENCY_HUF = getattr(django_settings, 'MULTICURRENCY_HUF', default_settings.CURRENCY_HUF)
CURRENCY_PLN = getattr(django_settings, 'MULTICURRENCY_PLN', default_settings.CURRENCY_PLN)
CURRENCY_RON = getattr(django_settings, 'MULTICURRENCY_RON', default_settings.CURRENCY_RON)
CURRENCY_GBP = getattr(django_settings, 'MULTICURRENCY_GBP', default_settings.CURRENCY_GBP)
CURRENCY_BGN = getattr(django_settings, 'MULTICURRENCY_BGN', default_settings.CURRENCY_BGN)

CURRENCY_CHOICES = getattr(django_settings, 'MULTICURRENCY_CURRENCY_CHOICES', default_settings.CURRENCY_CHOICES)
CURRENCY_SIGNS = getattr(django_settings, 'MULTICURRENCY_CURRENCY_SIGNS', default_settings.CURRENCY_SIGNS)

SOURCE_ECB = getattr(django_settings, 'MULTICURRENCY_SOURCE_ECB', default_settings.SOURCE_ECB)
SOURCE_CNB = getattr(django_settings, 'MULTICURRENCY_SOURCE_CNB', default_settings.SOURCE_CNB)
SOURCE_NBP = getattr(django_settings, 'MULTICURRENCY_SOURCE_NBP', default_settings.SOURCE_NBP)
SOURCE_MNB = getattr(django_settings, 'MULTICURRENCY_SOURCE_MNB', default_settings.SOURCE_MNB)
SOURCE_RNB = getattr(django_settings, 'MULTICURRENCY_SOURCE_RNB', default_settings.SOURCE_RNB)
SOURCE_BOE = getattr(django_settings, 'MULTICURRENCY_SOURCE_BOE', default_settings.SOURCE_BOE)

EXCHANGE_RATES_SOURCES = getattr(django_settings, 'MULTICURRENCY_EXCHANGE_RATES_SOURCES', default_settings.EXCHANGE_RATES_SOURCES)
CURRENCY_RATE_SOURCES = getattr(django_settings, 'MULTICURRENCY_CURRENCY_RATE_SOURCES', default_settings.CURRENCY_RATE_SOURCES)
NATIONAL_BANKS = getattr(django_settings, 'MULTICURRENCY_NATIONAL_BANKS', default_settings.NATIONAL_BANKS)
AVAILABLE_RATE_SOURCES = getattr(django_settings, 'MULTICURRENCY_AVAILABLE_RATE_SOURCES', default_settings.AVAILABLE_RATE_SOURCES)
BASE_CURRENCY = getattr(django_settings, 'MULTICURRENCY_BASE_CURRENCY', default_settings.BASE_CURRENCY)
