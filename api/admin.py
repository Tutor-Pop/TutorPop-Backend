from django.contrib import admin
from api.models import Account,School

class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_id','username','firstname','lastname','email','is_verified','is_deleted']
    search_fields = ['username','firstname','lastname']
    list_filter = ['is_verified','is_deleted']

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['school_id','owner_id','name','address']

admin.site.register(Account,AccountAdmin)
admin.site.register(School,SchoolAdmin)
