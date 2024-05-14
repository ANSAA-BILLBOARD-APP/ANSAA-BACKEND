from django.contrib import admin
from . models import Billboards, Zones, UserZone
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models



class BillboardsAdminConfig(admin.ModelAdmin):
    model = Billboards
    search_fields = ('agent','company','city','dimension','asset_name')
    list_filter = ('company', 'status','vacancy','city')
    ordering = ('-vacancy',)
    list_display = ('agent','asset_name','company','price')
    fieldsets = (
        (None, {'fields': ('asset_name','address','city','company','phone_number', 'dimension','price','picture',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('asset_name','company', 'agent', 'city')}
         ),
    )


admin.site.register(Billboards)
admin.site.register(Zones)
admin.site.register(UserZone)
