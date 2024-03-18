from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Customer_req', views.Customer_req, name="Customer_req"),
    path('customer/<str:pk>', views.customer_page, name='customer'),
    path('delete_order/<str:pk>', views.delete_order, name="order"),
    path('add_materials', views.add_materials, name='add_materials'),
    path('alec_api', views.apitest, name='materials'),
    path('list_customers', views.list_customers,name='list_customers'),
    path('create_customer', views.create_customer,name='create_customer'),
    path('update_customer', views.update_customer,name='update_customer'),
    path('get_customer/<int:pk>/', views.get_customer,name='get_customer'),
    path('list_invoices', views.list_invoices,name='list_invoices'),
    path('list_suppliers', views.list_suppliers,name='list_suppliers'),
    path('list_inventorys', views.list_inventorys,name='list_inventorys'),
    path('list_orders', views.list_orders,name='list_orders'),
    path('list_quotations', views.list_quotations,name='list_quotations'),
    path('list_revenue', views.list_revenue,name='list_revenue')
]
