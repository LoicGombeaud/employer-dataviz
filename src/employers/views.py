from django.contrib.auth import get_user
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from rules.contrib.views import permission_required, objectgetter


from .models import Employer, Site

def index(request):
    employers_list = list(filter(lambda e: get_user(request).has_perm("employers.view_employer", e),
                                 Employer.objects.all()))
    territories_list = set(map(lambda e: e.territory,
                               employers_list))
    territory_to_employers_dict = {}
    for territory in territories_list:
        territory_to_employers_dict[territory] = list(filter(lambda e: e.territory == territory,
                                                             employers_list))
    context = {
        "territory_to_employers_dict": territory_to_employers_dict,
    }
    print(territory_to_employers_dict)
    return render(request, "employers/index.html", context)

@permission_required("employers.view_employer", fn=objectgetter(Employer, "employer_id"))
def detail(request, employer_id):
    employer = Employer.objects.get(id=employer_id)
    context = {
        "employer": employer,
    }
    return render(request, "employers/detail.html", context)

def get_employer_by_site_id(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    return get_object_or_404(Employer, id=site.employer.id)

@permission_required("employers.view_employer", fn=get_employer_by_site_id)
def site(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    context = {
        "site": site,
    }
    return render(request, "sites/detail.html", context)

@permission_required("employers.view_employer", fn=get_employer_by_site_id)
def edit_site(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    try:
        employee_street_addresses_list = request.POST["employee_street_addresses"].splitlines()
        site.update_addresses(employee_street_addresses_list)
        return HttpResponseRedirect(reverse("employers:edit_site", args=site_id))
    except:
        pass
    employee_street_addresses_list = map(lambda e: e.address.street_address,
                                         site.employee_set.all())
    context = {
        "site": site,
        "employee_street_addresses": "\n".join(employee_street_addresses_list),
    }
    return render(request, "sites/edit.html", context)
