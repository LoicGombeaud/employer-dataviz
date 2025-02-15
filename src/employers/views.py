from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Employer

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
