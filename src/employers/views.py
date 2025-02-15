from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader


from .models import Employer, Site

def index(request):
    employers_list = Employer.objects.all()
    context = {
        "employers_list": employers_list,
    }
    return render(request, "employers/index.html", context)

def detail(request, employer_id):
    employer = Employer.objects.get(id=employer_id)
    context = {
        "employer": employer,
    }
    return render(request, "employers/detail.html", context)

def site(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    try:
        employee_street_addresses_list = request.POST["employee_street_addresses"].splitlines()
        site.update_addresses(employee_street_addresses_list)
    except:
        pass
    employee_street_addresses_list = map(lambda e: e.address.street_address,
                                         site.employee_set.all())
    context = {
        "site": site,
        "employee_street_addresses": "\n".join(employee_street_addresses_list),
    }
    return render(request, "sites/detail.html", context)
