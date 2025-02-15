from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:employer_id>", views.employer, name="employer")
]
