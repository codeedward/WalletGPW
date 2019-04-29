from django.urls import path
from . import views

urlpatterns = [
    path('wallet/loadData/', views.LoadData, name='wallet-loadData'),
    path('wallet/shareDetails/<str:shareName>', views.ShareDetails, name='wallet-shareDetails'),
    path('', views.Dashboard, name='wallet-dashboard'),
]
