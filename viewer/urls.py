from django.urls import path

from . import views

app_name = "viewer"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="homepage"),
    path("renew/", views.renew, name="renew"),
]
