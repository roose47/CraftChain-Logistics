from django.urls import path
from . import views
from .views import CustomerCreateView

urlpatterns = [
    path('', views.home, name='home'),
    path('Customer_req', views.Customer_req, name="Customer_req"),
    path('customer/<str:pk>', views.customer_page, name='customer'),
    path('delete_order/<str:pk>', views.delete_order, name="order"),
    path('add_materials', views.add_materials, name='add_materials'),
<<<<<<< Updated upstream
    path('json', views.json, name='json')
=======
    path('alec_api', views.apitest, name='materials'),
    path('list_customers', views.list_customers,name='list_customers'),
    path('create_customer', views.add_customer,name='add_customer'),
    path('list_orders', views.list_orders,name='add_customer'),
    path('list_suppliers', views.list_suppliers,name='list_suppliers'),
    path('list_invoices', views.list_invoices,name='list_invoices')
    # path('api/customers/', CustomerCreateView.as_view(), name='customer-create')
>>>>>>> Stashed changes
]
