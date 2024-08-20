from django.contrib import admin

from users.models import Balance


@admin.register(Balance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    readonly_fields = ('user',)
