from django.contrib import admin

from .models import UserC, Friend


# Register your models here.

class FriendInline(admin.TabularInline):
    model = Friend
    fk_name = 'user'


class UserAdmin(admin.ModelAdmin):
    inlines = [FriendInline]


admin.site.register(UserC, UserAdmin)
admin.site.register(Friend)
