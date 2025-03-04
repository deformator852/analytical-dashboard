from django.urls import path

from dashboard.views import DashBoard

urlpatterns = [
    path("dashboard/", DashBoard.as_view()),
]
