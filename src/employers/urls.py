from django.urls import path

from . import views

app_name = "employers"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:employer_id>", views.detail, name="detail"),
    path("site/<int:site_id>", views.site, name="site"),
]
