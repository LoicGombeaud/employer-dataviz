from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the employer management index.")
