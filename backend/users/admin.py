from django.contrib import admin

from .models import Subscription, User


@admin.register(Subscription)
class SubscriptonAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user__username', 'author__username')
    empty_value_display = '-пусто-'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'