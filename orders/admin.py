from django.contrib import admin
from .models import TelegramUser


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id',)
    search_fields = ('chat_id',)


admin.site.register(TelegramUser, TelegramUserAdmin)
