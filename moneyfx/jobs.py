# ECB RATES (EUROPE)
from datetime import date, datetime
from decimal import Decimal

import requests
import xml.etree.ElementTree as ET

from django.core.mail import send_mail
from rest_framework import status

from moneyfx import conf
from moneyfx.models import ExchangeRate
from moneyfx.serializers import ExchangeRateSerializer


def save_exchange_rates():
    url_ecb = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    response = requests.get(url=url_ecb)
    namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    rates = {}
    today = date.today()
    tree = ET.fromstring(response.text)

    if response.status_code != status.HTTP_200_OK:
        notify_admins_if_error('Response status code from ECB: %s' % response.status_code)

    date_ecb_str = tree.find('.//ex:Cube[@time]', namespaces=namespaces).get('time')
    for cube in tree.findall('.//ex:Cube[@currency]', namespaces=namespaces):
        currency = cube.attrib['currency']
        rate = cube.attrib['rate']
        if conf.DEBUG:
            print(currency, rate)
        rate = round(float(rate), 4)
        rates['c_' + currency.lower()] = rate

    if conf.DEBUG:
        print(response)
    rates['validity_date'] = today
    rates['created_date'] = date_ecb_str

    serializer = ExchangeRateSerializer(data=rates)
    if not ExchangeRate.objects.filter(validity_date=today).exists():
        if serializer.is_valid():
            serializer.save()
        else:
            notify_admins_if_error("Invalid serializer data in ECB save exchange rate method.")


# CNB RATES (CZECH)
def save_cnb_rates(rate_date=None):
    rates = {}
    exchange_rate = ExchangeRate()

    if rate_date is None:
        rate_date = date.today()

    rate_date_for_url = rate_date.strftime("%d.%m.%Y")
    cnb_url = f'https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date={rate_date_for_url}'
    response = requests.get(url=cnb_url)

    for index, line in enumerate(response.text.splitlines()):
        if index == 0:  # create date
            created_date = line.split(' ')[0]
            created_date_obj = datetime.strptime(created_date, '%d.%m.%Y').date()
            rates['validity_date'] = created_date_obj
            rates['created_date'] = created_date_obj
        elif index == 1:  # header
            continue
        else:  # current currency data
            line_split = line.split('|')
            currency_amount = line_split[2]
            currency = line_split[3]

            rate = Decimal(line_split[4].replace(',', '.'))
            currency_name = 'c_' + currency.lower()
            rates[currency_name] = rate

            currency_amount_name = currency_name + '_amount'

            if hasattr(exchange_rate, currency_amount_name):
                rates[currency_amount_name] = int(currency_amount)

            rates['fixed_base_currency'] = False
            rates['source'] = conf.SOURCE_CNB

    serializer = ExchangeRateSerializer(data=rates)
    if not ExchangeRate.objects.filter(validity_date=created_date_obj, source=rates['source']).exists():
        if serializer.is_valid():
            serializer.save()
        else:
            notify_admins_if_error("Invalid serializer data.")


# NBP RATES (POLAND)
def save_nbp_rates():
    pnb_dir_url = 'https://static.nbp.pl/dane/kursy/xml/dir.txt'
    dir_response = requests.get(url=pnb_dir_url)
    actual_dir = get_actual_dir(dir_response)

    save_nbp_rates_from_dir(actual_dir)


def save_nbp_rates_from_dir(dir):
    rates = {}
    pnb_url = f'https://static.nbp.pl/dane/kursy/xml/{dir}.xml'
    rates_response = requests.get(url=pnb_url)
    tree = ET.fromstring(rates_response.text)

    created_date = tree.find('data_publikacji').text
    created_date_obj = datetime.strptime(created_date, '%Y-%m-%d').date()
    rates['validity_date'] = created_date_obj
    rates['created_date'] = created_date_obj

    for xml_rate in tree.findall('pozycja'):
        currency_amount = xml_rate[1].text
        currency_code = xml_rate[2].text.lower()
        currency_rate = Decimal(xml_rate[3].text.replace(',', '.'))

        rates['c_' + currency_code] = currency_rate
        rates['c_' + currency_code + '_amount'] = int(currency_amount)
        rates['fixed_base_currency'] = False
        rates['source'] = conf.SOURCE_NBP

    serializer = ExchangeRateSerializer(data=rates)

    if not ExchangeRate.objects.filter(validity_date=created_date_obj, source=rates['source']).exists():

        if serializer.is_valid():
            serializer.save()
        else:
            notify_admins_if_error("Invalid serializer data.")


def get_actual_dir(dirs):
    dirs_list = dirs.text.splitlines()
    dirs_list.reverse()

    for actual_dir in dirs_list:

        if actual_dir[0] == 'a':
            return actual_dir

    return None


def notify_admins_if_error(error_message):
    from django.conf import settings
    subject = 'ERROR: get exchange rates failed'
    recipients = [a[1] for a in settings.ADMINS]
    message = 'Some errors occurred during cron job, which updates the exchange rates table on daily basis: %s.' % error_message
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)