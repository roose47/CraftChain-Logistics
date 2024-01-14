from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Customer_req', views.Customer_req, name="Customer_req"),
    path('customer/<str:pk>', views.customer_page, name='customer'),
    path('delete_order/<str:pk>', views.delete_order, name="order"),
    path('add_materials', views.add_materials, name='add_materials'),
    path('json', views.json, name='json')
]
