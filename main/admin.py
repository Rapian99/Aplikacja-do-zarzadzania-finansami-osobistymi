from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    def must_change_password(self, obj):
        return obj.userprofile.must_change_password

    must_change_password.boolean = True
    must_change_password.short_description = "Must Change Password"

    list_display = (
        "username",
        "email",
        "first_name",
        "is_staff",
        "must_change_password",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
