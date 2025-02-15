from django.contrib import admin

from .models import Address, Employee, Employer, Site, Territory

admin.site.register(Address)
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(Site)
admin.site.register(Territory)
