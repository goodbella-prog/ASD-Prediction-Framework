from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path("evaluation/", views.evaluation, name="evaluation"),
    path("export-pdf/", views.export_pdf, name="export_pdf"),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("history/", views.history, name="history"),
]

