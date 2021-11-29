from django.contrib import admin
from application.models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'phone', 'is_staff', 'user_type', 'profile_picture'
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('user_type', 'profile_picture')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('user_type', 'profile_picture')
        })
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Clinic)
admin.site.register(Social)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Nurse)
admin.site.register(Day)
admin.site.register(Availability)


