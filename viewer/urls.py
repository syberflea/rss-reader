from django.urls import path

from .views import HomePageView

app_name = 'viewer'

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
]
