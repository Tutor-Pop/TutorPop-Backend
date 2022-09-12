from django.contrib import admin
from api.models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_id','username','firstname','lastname','email','is_verified','user_status']
    search_fields = ['username','firstname','lastname']
    list_filter = ['is_verified','user_status']

admin.site.register(Account,AccountAdmin)