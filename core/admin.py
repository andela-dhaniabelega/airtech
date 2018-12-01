from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import CreateUserForm, ChangeUserForm
from core.models import User, Flight, Ticket


class CustomUserAdmin(UserAdmin):
    add_form = CreateUserForm
    form = ChangeUserForm
    model = User
    list_display = ['email', 'first_name', 'last_name', 'date_of_birth', 'photo']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'date_of_birth', 'photo'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Flight)
admin.site.register(Ticket)
