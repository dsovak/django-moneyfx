from django.contrib import admin
from moneyfx.models import ExchangeRate

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('validity_date', 'source', 'c_eur', 'c_usd', 'c_gbp', 'created')
    list_filter = ('source', 'validity_date')
    search_fields = ('validity_date',)
