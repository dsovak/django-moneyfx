from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MoneyfxConfig(AppConfig):
    name = 'moneyfx'
    verbose_name = _('Money FX')