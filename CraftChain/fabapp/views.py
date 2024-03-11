from django.shortcuts import render, redirect
from django.http import HttpResponse
<<<<<<< Updated upstream
from .models import CustomerRequirements, Inventory
=======
from .models import CustomerRequirements, Inventory, Customer, Order, Supplier, Invoice
>>>>>>> Stashed changes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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


def json(request):
    data = list(CustomerRequirements.objects.values())
    data2 = list(Inventory.objects.values())
    big_data = [data,data2]
<<<<<<< Updated upstream
    return JsonResponse(big_data, safe=False)
=======
    return JsonResponse(data, safe=False)

def list_customers(request):
    customer_db = Customer.objects.all()
    all_customers = list ()
    for customer in customer_db:
        all_customers.append({
            'name':customer.name,
            'email':customer.email,
            'phone_number':customer.phone_number
        })
    all_customers = list(all_customers)
    return JsonResponse(all_customers, safe=False)

def list_orders(request):
    order_db = Order.objects.all()
    all_orders = list()
    for order in order_db:
        all_orders.append({
            'customer':order.customer.name,
            'order_name':order.order_name,
            'order_id':order.order_id,
            'date':order.date,
            'order_status':order.order_status
        })

    return JsonResponse(all_orders, safe=False)

def list_suppliers(request):
    suppliers_db = Supplier.objects.all()
    all_suppliers = list()
    for supplier in suppliers_db:
        all_suppliers.append({
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
            'customer_name': invoice.customer_name
        })
    return JsonResponse(all_invoices, safe=False)

@csrf_exempt
def add_customer(request):
    if request.method=="POST":
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')

        if not name or not email or not phone_number:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        customer = Customer.objects.create(name=name, email=email, phone_number=phone_number)
        return JsonResponse({'message': 'Customer created successfully', 'customer_id': customer.id}, status=201)    
    



#
#
#
# 
# 
# 
# 
# 


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

# @method_decorator(csrf_exempt, name='dispatch')
class CustomerCreateView(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')

        if not name or not email or not phone_number:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        customer = Customer.objects.create(name=name, email=email, phone_number=phone_number)
        return JsonResponse({'message': 'Customer created successfully', 'customer_id': customer.id}, status=201)
>>>>>>> Stashed changes
