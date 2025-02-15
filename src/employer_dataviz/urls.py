from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("employers/", include("employers.urls")),
    path("admin/", admin.site.urls),
]
