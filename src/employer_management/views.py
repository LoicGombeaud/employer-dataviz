from django.http import HttpResponse

from .models import Employer

def index(request):
    return HttpResponse("This is the employer management index.")

def employer(request, employer_id):
    employer = Employer.objects.get(id=employer_id)
    return HttpResponse(f"Employer #{employer_id}: {employer.name}")
