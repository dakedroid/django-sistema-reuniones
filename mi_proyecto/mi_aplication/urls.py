from django.urls import path
from . import views 

urlpatterns = [
    path("lista/", views.lista.as_view(), name = "milista")
]
