from django.contrib import admin

from .models import Club, Player, Transfer


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "founded_year"]
    search_fields = ["name", "country"]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["name", "nationality", "position", "current_club"]
    list_filter = ["position", "nationality"]
    search_fields = ["name"]


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ["player", "origin_club", "destination_club", "transfer_date", "transfer_fee"]
    list_filter = ["transfer_date"]
    search_fields = ["player__name"]
