# Register your models here.

from django.contrib import admin

from .models import FortiGroup, FortiParameters
from .forms import FortiParametersAdminForm

class FortiGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled')

class FortiParametersAdmin(admin.ModelAdmin):
    list_display = ('fortiIP', 'fortiPort', 'fortiVdom', 'fortiUserName', 'fortiDefaultGroupName', 'fortiAccessEnabledGroupName', 'fortiKeyStorePath')
    form = FortiParametersAdminForm

admin.site.register(FortiGroup, FortiGroupAdmin)
admin.site.register(FortiParameters, FortiParametersAdmin)

