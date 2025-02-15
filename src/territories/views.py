from django.shortcuts import render


def index(request):
    return render(request, "base.html")

def detail(request):
    return render(request, "base.html")
