from django.contrib import admin

# Register your models here.

from .models import CustomerRequirements, Inventory, Supplier,Customer, Order, Invoice,Quotation


class CustomerReqAdmin(admin.ModelAdmin):
    list_display=('name','created_at','updated_at')
    search_fields =('name','desc')
    list_per_page=10


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date')

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'date')


class QuotationAdmin(admin.ModelAdmin):
    list_display = ('quotation_name', 'date')



# class InvoiceAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'amount', 'date','status')
#     readonly_fields = ('date',)



admin.site.register(CustomerRequirements,CustomerReqAdmin)
admin.site.register(Inventory)
admin.site.register(Supplier)
admin.site.register(Order,OrderAdmin)
admin.site.register(Customer)
admin.site.register(Invoice,InvoiceAdmin)
admin.site.register(Quotation,QuotationAdmin)