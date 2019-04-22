from django.urls import path
from . import views

urlpatterns = [
    path('wallet/loadData/', views.LoadData, name='wallet-loadData'),
    path('', views.Dashboard, name='wallet-dashboard'),
]
