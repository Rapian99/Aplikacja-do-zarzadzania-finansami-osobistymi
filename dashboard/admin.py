from django.contrib import admin
from .models import Currency, UserCurrencyData, Account, Categories, Transaction, WishlistItem


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "symbol", "exchange_rate")
    search_fields = ("name", "symbol")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "created_at")
    search_fields = ("user__username", "name")


@admin.register(UserCurrencyData)
class UserCurrencyDataAdmin(admin.ModelAdmin):
    list_display = ("user", "currency", "account", "amount")
    search_fields = ("user__username", "currency__name", "account__name")


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    search_fields = ("name", "type")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "account",
        "currency",
        "category",
        "amount",
        "transaction_type",
        "date",
    )
    search_fields = ("user__username", "account__name", "currency__name")
    list_filter = ("transaction_type", "date")


