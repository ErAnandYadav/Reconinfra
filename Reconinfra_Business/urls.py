


from django.urls import path
from .import views

urlpatterns = [
    path('Emi_module/', views.Business_Home, name="BusinessHome" )
]
