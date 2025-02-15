from django.contrib import admin

from employers.models import Address, Employee, Employer, Site


admin.site.register(Address)
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(Site)
