from django.contrib import admin
from authentication.models import AnsaaUser, OTP
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = AnsaaUser
    search_fields = ('user_id','email','fullname','phone_number', 'gender')
    list_filter = ('is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('user_id','email','fullname','phone_number','is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('password','email','fullname','phone_number', 'gender', 'picture','last_login',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'phone_number', 'gender', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )




admin.site.register(AnsaaUser, UserAdminConfig)
admin.site.register(OTP)
