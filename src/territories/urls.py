from django.urls import path

from . import views


app_name = "territories"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:territory_id>", views.detail, name="detail"),
]
