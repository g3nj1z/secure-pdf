from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", views.index, name="index"),
    path("media/pdf/<str:file>", views.securePdf, name="secure"),
    path("generate-pdf/", views.generate_pdf, name="generate_pdf"),
]
