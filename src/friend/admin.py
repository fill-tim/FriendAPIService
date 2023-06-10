from django.contrib import admin

from .models import User, Friend, FriendRequest


# Register your models here.

class FriendInline(admin.TabularInline):
    model = Friend
    fk_name = 'user'


class OutgoingFriendRequestInline(admin.TabularInline):
    model = FriendRequest
    fk_name = 'from_whom'


class IncomingFriendRequestInline(admin.TabularInline):
    model = FriendRequest
    fk_name = 'to_whom'


class UserAdmin(admin.ModelAdmin):
    inlines = [FriendInline, OutgoingFriendRequestInline, IncomingFriendRequestInline]


admin.site.register(User, UserAdmin)
admin.site.register(Friend)

admin.site.register(FriendRequest)
