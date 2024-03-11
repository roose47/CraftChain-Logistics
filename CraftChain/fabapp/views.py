from collections import OrderedDict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomerRequirements, Inventory, Customer,Invoice, Order, Supplier,Quotation
from django.http import JsonResponse
# Create your views here.


def home(request):
    all_orders = CustomerRequirements.objects.all()
    total_orders = all_orders.count()
    params = {'name': 'Roose', 'roll': 2, 'orders': all_orders}
    return render(request, "home.html", params)


def delete_order(request,pk):
    order = CustomerRequirements.objects.get(id=pk)
    context = {'orders':order}
    if request.method == "POST":
        order.delete()
        return redirect('/')
    return render(request, "delete.html", context)

def customer_page(request, pk):
    customer = CustomerRequirements.objects.get(id=pk)
    desc = customer.desc
    params = {'description': desc}
    return render(request, "customer.html", params)


def Customer_req(request):
    if request.method == 'POST':
        name = request.POST['fname']
        contact = request.POST['contact']
        email = request.POST['email']
        desc = request.POST['description']

        new_req = CustomerRequirements(name=name, phone=contact, email=email, desc=desc)
        new_req.save()
        return redirect('/')
    return render(request, "requirements.html", {})


def add_materials(request):
    choices = Inventory.MATERIAL_CHOICES

    if request.method == 'POST':
        material = request.POST.get('material_name')
        print(material)
        # material = request.POST['id_material_name']
        mat_amount = request.POST['mat_amount']
        # Validate and process the data as needed
        Inventory(material_name=material, material_amt=mat_amount).save()
        return redirect('/')  # Redirect to a success page or another URL

    return render(request, 'inventory.html', {'choices': choices})


def apitest(request):
    data = list(CustomerRequirements.objects.values())
    data2 = list(Inventory.objects.values())
    big_data = [data,data2]
    return JsonResponse(data, safe=False)

def list_customers(request):
    all_customers = list(Customer.objects.values())
    return JsonResponse(all_customers, safe=False)

def list_invoices(request):
    all_invoices = list(Invoice.objects.values())
    return JsonResponse(all_invoices, safe=False)

def list_suppliers(request):
    all_suppliers= list(Supplier.objects.values())
    return JsonResponse(all_suppliers, safe=False)

def list_inventorys(request):
    all_inventorys= list(Inventory.objects.values())
    return JsonResponse(all_inventorys, safe=False)

def list_orders(request):
    all_orders= list(Order.objects.values())
    return JsonResponse(all_orders, safe=False)

def list_quotations(request):
    all_quotations= list(Quotation.objects.values())
    return JsonResponse(all_quotations, safe=False)

