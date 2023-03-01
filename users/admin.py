from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users import models
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'role']
    fieldsets = (
        (None, {
            "fields": (
                "email",
                "password"
            ),
        }),
        (
            _("Roles"), {
                "fields": (
                    "role",
                )
            }
        ),
        (
            _("Permissions"), {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            }
        ),
        (
            _("Important Dates"), {
                "fields": (
                    "last_login",
                )
            }
        )
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "role",
                "is_active",
                "is_staff",
                "is_superuser",
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Patient)
admin.site.register(models.Doctor)
admin.site.register(models.Admin)
