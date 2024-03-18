from collections import OrderedDict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import CustomerRequirements, Inventory, Customer,Invoice, Order, Supplier,Quotation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.


def home(request):
    all_orders = CustomerRequirements.objects.all()
    total_orders = all_orders.count()
    params = {'name': 'Roose', 'roll': 2, 'orders': all_orders}
    return render(request, "home.html", params)




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
    customer_db = Customer.objects.all()
    all_customers = list ()
    for customer in customer_db:
        all_customers.append({
            'id':customer.id,
            'name':customer.name,
            'email':customer.email,
            'phone_number':customer.phone_number
        })
    all_customers = list(all_customers)
    return JsonResponse(all_customers, safe=False)

@csrf_exempt
def create_customer(request):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        name=data.get('name')
        email=data.get('email')
        phone_number=data.get('phone_number')
        Customer.objects.create(
            name=name,
            email=email, 
            phone_number=phone_number
        )
        return HttpResponse()

def get_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    data = {
        'id': customer.pk,
        'name': customer.name,
        'email': customer.email,
        'phone_number':customer.phone_number
    }
    return JsonResponse(data)


@csrf_exempt
def update_customer(request):
    print("I was called")
    if request.method == 'POST':
        print("I have passed the condition check")
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        id = data.get('id')
        name=data.get('name')
        email=data.get('email')
        phone_number=data.get('phone_number')
        customer=Customer.objects.get(id=id)
        customer.name=name
        customer.email=email
        customer.phone_number=phone_number
        customer.save()
    return HttpResponse()


# @csrf_exempt
# def delete_customer(request):
#     if request.method == 'DELETE':
#         data = json.loads(request.body.decode('utf-8'))
#         print(data)
#         customer_id = data.get('customer_id')
#         try:
#             customer = Customer.objects.get(id=customer_id)
#             customer.delete()
#             return JsonResponse({'message': 'Customer deleted successfully'}, status=204)
#         except Customer.DoesNotExist:
#             return JsonResponse({'error': 'Customer not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)


def list_orders(request):
    order_db = Order.objects.all()
    all_orders = list()
    for order in order_db:
        all_orders.append({
            'customer':order.customer.name,
            'order_name':order.order_name,
            'id':order.order_id,
            'date':order.date,
            'order_status':order.order_status
        })

    return JsonResponse(all_orders, safe=False)


@csrf_exempt
def create_order(request):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        customer=data.get('customer_name')
        order_name=data.get('order_name')
        status = data.get('status')
        Order.objects.create(
            customer=Customer.objects.get(name=customer),
            order_name=order_name, 
            order_status=status
        )
        return HttpResponse()

def get_order(request, pk):
    order = Order.objects.get(order_id=pk)
    customer_obj = order.customer
    customer_name = customer_obj.name
    data = {
        "customer_name":customer_name,
        "order_name":order.order_name,
        "id":order.order_id,
        "date":order.date,
        "order_status":order.order_status
    }

    return JsonResponse(data) 

@csrf_exempt
def update_order(request):
    print("update order was called")
    if request.method == 'POST':
        print("I am post methjod")
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        order_id = data.get('order_id')
        order_name= data.get('order_name')
        order_status= data.get('order_status')

        order_obj =Order.objects.get(order_id=order_id)
        order_obj.order_name = order_name
        order_obj.order_status = order_status
        order_obj.save()

    return HttpResponse()


@csrf_exempt
def delete_order(request, pk):

    if request.method == 'DELETE':
        # data = json.loads(request.body.decode('utf-8'))
        # print(data)
        # customer_id = data.get('customer_id')
        try:
            order = Order.objects.get(order_id=pk)
            order.delete()
            return JsonResponse({'message': 'Order deleted successfully'}, status=204)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)





def list_suppliers(request):
    suppliers_db = Supplier.objects.all()
    all_suppliers = list()
    for supplier in suppliers_db:
        all_suppliers.append({
            'supplier_id':supplier.id,
            'supplier_name':supplier.supplier_name,
            'email':supplier.email,
            'phone':supplier.phone,
            'rating':supplier.rating
        })
    return JsonResponse(all_suppliers, safe=False)
    
def list_invoices(request):
    invoices_db = Invoice.objects.all()
    all_invoices = []
    for invoice in invoices_db:
        all_invoices.append({
            'order_id': invoice.order_id,
            'invoice_amount': invoice.invoice_amount,
            'address': invoice.address,
            'date':invoice.date,
            'customer_name': invoice.customer_name,
            'invoice_status':invoice.order_status
        })
    return JsonResponse(all_invoices, safe=False)

def list_inventorys(request):
    inventory_db = Inventory.objects.all()
    all_inventorys= list()
    for material in inventory_db:
        all_inventorys.append({
            'material_id':material.id,
            'material_name':material.material_name,
            'material_amt':material.material_amt
        })
    return JsonResponse(all_inventorys, safe=False)


def list_quotations(request):
    quotation_db= Quotation.objects.all()
    all_quotations=list()
    for quotation in quotation_db:
        all_quotations.append({
            'qoutation_id':quotation.id,
            'quotation_name':quotation.quotation_name,
            'supplier_name':quotation.supplier.supplier_name,
            'date':quotation.date,
            'quotation_status':quotation.quotation_status
        })
    return JsonResponse(all_quotations, safe=False)

def get_suppliers(request, pk):
    supplier = Supplier.objects.get(id=pk)
    data = {
        "supplier_id":supplier.id,
        "supplier_name":supplier.supplier_name,
        "phone":supplier.phone,
        "email":supplier.email,
        "rating":supplier.rating
    }

    return JsonResponse(data)

@csrf_exempt
def create_suppliers(request):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        supplier_name=data.get('supplier_name')
        email=data.get('email')
        phone=data.get('phone')
        rating= data.get('rating')
        Supplier.objects.create(
            supplier_name=supplier_name,
            email=email, 
            phone=phone,
            rating= rating
        )
        return HttpResponse()

@csrf_exempt
def update_suppliers(request):
    print("update suppliers was called")
    if request.method == 'POST':
        print("I am post methjod")
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        supplier_id = data.get('supplier_id')
        supplier_name= data.get('supplier_name')
        phone= data.get('phone')
        email= data.get('email')
        rating= data.get('rating')

        supplier_obj =Supplier.objects.get(id=supplier_id)
        supplier_obj.supplier_name = supplier_name
        supplier_obj.phone = phone
        supplier_obj.email = email
        supplier_obj.rating = rating
        supplier_obj.save()

    return HttpResponse()

@csrf_exempt
def delete_supplier(request, pk):

    if request.method == 'DELETE':
        # data = json.loads(request.body.decode('utf-8'))
        # print(data)
        # customer_id = data.get('customer_id')
        try:
            supplier = Supplier.objects.get(id=pk)
            supplier.delete()
            return JsonResponse({'message': 'Supplier deleted successfully'}, status=204)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Supplier not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)