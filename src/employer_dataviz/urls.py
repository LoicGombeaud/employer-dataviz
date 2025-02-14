from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("employers/", include("employer_management.urls")),
    path("admin/", admin.site.urls),
]
