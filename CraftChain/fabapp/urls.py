from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Customer_req', views.Customer_req, name="Customer_req"),
    path('customer/<str:pk>', views.customer_page, name='customer'),
    # path('delete_order/<str:pk>', views.delete_order, name="order"),
    path('add_materials', views.add_materials, name='add_materials'),
    path('alec_api', views.apitest, name='materials'),
    path('list_customers', views.list_customers,name='list_customers'),
    path('create_customer', views.create_customer,name='create_customer'),
    path('update_customer', views.update_customer,name='update_customer'),
    path('get_customer/<int:pk>/', views.get_customer,name='get_customer'),
    # path('delete_customer', views.delete_customer,name='delete_customer'),
    path('list_invoices', views.list_invoices,name='list_invoices'),
    path('list_suppliers', views.list_suppliers,name='list_suppliers'),
    path('delete_supplier/<int:pk>/', views.delete_supplier,name='delete_supplier'),
    path('create_suppliers', views.create_suppliers,name='create_suppliers'),
    path('get_suppliers/<int:pk>/', views.get_suppliers,name='get_suppliers'),
    path('update_suppliers', views.update_suppliers,name='update_suppliers'),
    path('list_inventorys', views.list_inventorys,name='list_inventorys'),
    path('list_orders', views.list_orders,name='list_orders'),
    path('create_order', views.create_order,name='create_order'),
    path('get_order/<int:pk>/', views.get_order,name='get_order'),
    path('delete_order/<int:pk>/', views.delete_order,name='delete_order'),
    path('update_order', views.update_order,name='update_order'),

    path('list_quotations', views.list_quotations,name='list_quotations')
]
