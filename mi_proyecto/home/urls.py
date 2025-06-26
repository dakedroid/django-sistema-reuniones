from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="nosotros"),
    path("contact/", views.contact, name="contacto"),
    path("sistemas/", views.sistemas, name="sistemas"),
    path("desarrolloapps/", views.desarrolloapps, name="desarrolloapps"),
]
