from django.contrib import admin

from .models import Employer, EmployerSite, Address

admin.site.register(Employer)
admin.site.register(EmployerSite)
admin.site.register(Address)
