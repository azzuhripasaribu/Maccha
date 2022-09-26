from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.forms import UserAdminCreationForm, UserAdminChangeForm

Account = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'admin']
    list_filter = ['admin', 'active', 'staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Full Name', {'fields': ('full_name',)}),
        ('Username', {'fields': ('username',)}),
        ('Company Name', {'fields': ('company_name',)}),
        ('Permissions', {'fields': ('admin', 'active', 'staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ['email', 'username', 'full_name']
    ordering = ['email']
    filter_horizontal = ()

admin.site.register(Account, UserAdmin)