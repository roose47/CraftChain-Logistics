from collections import OrderedDict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import CustomerRequirements, Inventory, Customer,Invoice, Order, Supplier,Quotation, Salary, Employee, Attendance
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, math
from fabapp.ml import get_prediction, get_demand
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,  Spacer
from reportlab.lib.styles import getSampleStyleSheet
# Create your views here.

def dashboard_api(request):
    all_customer_objs = Customer.objects.all()
    total_invoices = Invoice.objects.all()
    paid_invoices = Invoice.objects.filter(invoice_status= "Paid").aggregate(total_invoices=Sum('invoice_amount'))['total_invoices']
    unpaid_invoices = Invoice.objects.filter(invoice_status= "Unpaid").aggregate(total_invoices=Sum('invoice_amount'))['total_invoices']
    if unpaid_invoices is None:
        unpaid_invoices = "All Paid"
    final_data = list()
    data = {
        "number_of_customers": len(all_customer_objs),
        "number_of_invoices":len(total_invoices),
        "paid_invoices": f"₹ {paid_invoices}",
        "unpaid_invoices":f"₹ {unpaid_invoices}",
         }
    final_data.append(data)
    return JsonResponse(final_data, safe=False)


def download_invoice_pdf(request, order_id):
    # Fetch invoice data from your database or any other source
    invoice_data = get_invoice_data(order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_data["Order_name"]}.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet ()
    # Add invoice data to the PDF
    elements.append(Paragraph("Invoice", styles['Heading1']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Company Name: Kondoth Fabrications", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Order_ID: {order_id}", styles["Normal"]))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(f"Order_name: {invoice_data['Order_name']}", styles["Normal"]))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(f"Invoice_amount: {invoice_data['Invoice_amount']}", styles["Normal"]))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(f"Address: {invoice_data['Address']}", styles["Normal"]))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(f"Customer_name: {invoice_data['Customer_name']}", styles["Normal"]))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(f"Date: {invoice_data['Date']}", styles["Normal"]))
    elements.append(Spacer(1, 5))
    # Add other fields from invoice_data to the PDF
    print("This is elements var ", elements )
    # Build the PDF document
    doc.build(elements)
    return response

def get_invoice_data(order_id):
    # Fetch and return invoice data from your database or any other source
    order_obj = Order.objects.get(order_id=order_id)
    invoice =Invoice.objects.get(order=order_obj)
    # invoice = Invoice.objects.get(id=order_id)
    data ={
        "Order_name": invoice.order.order_name,
        "Invoice_amount": invoice.invoice_amount,
        "Address": invoice.address,
        "Customer_name": invoice.customer_name,
        "Date": invoice.date
        }
    return data


def top_5_latest_invoices(request):
    # Fetch the top 5 latest invoices ordered by creation date
    latest_invoices = Invoice.objects.filter(invoice_status='Unpaid').order_by('date')[:5]
    final_data = list()
    for invoice in latest_invoices:
        customer_name = invoice.customer_name
        cust_obj =Customer.objects.get(name=customer_name)

        data ={
            "customer_id":cust_obj.id,
            "order_id":invoice.order.order_id,
            "customer_name":customer_name,
            "amount":invoice.invoice_amount,
        }
        final_data.append(data)
    
    # Render a template with the fetched invoices
    return JsonResponse(final_data, safe=False)


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

@csrf_exempt
def add_materials(request):

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        material_name=data.get('material_name')
        material_amount=data.get('material_amount')
        
        Inventory.objects.create(
            material_name=material_name,
            material_amt=material_amount
        )
        return HttpResponse()


def get_material(request, pk):
    material = get_object_or_404(Inventory, pk=pk)
    data = {
        'material_id': material.pk,
        'material_name': material.material_name,
        'material_amount': material.material_amt
    }
    return JsonResponse(data)

@csrf_exempt
def update_material(request):
    print("I was called")
    if request.method == 'POST':
        print("I have passed the condition check")
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        material_id = data.get('material_id')
        material_name=data.get('material_name')
        material_amt=data.get('material_amount')
        material_obj=Inventory.objects.get(id=material_id)
        material_obj.material_name=material_name
        material_obj.material_amt=material_amt
        material_obj.save()
    return HttpResponse()


@csrf_exempt
def delete_material(request, pk):

    if request.method == 'DELETE':
        # data = json.loads(request.body.decode('utf-8'))
        # print(data)
        # customer_id = data.get('customer_id')
        try:
            supplier = Inventory.objects.get(id=pk)
            supplier.delete()
            return JsonResponse({'message': 'materiak deleted successfully'}, status=204)
        except Inventory.DoesNotExist:
            return JsonResponse({'error': 'material not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



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
    order_status = request.GET.get('status', None)
    if order_status:
        order_db = Order.objects.filter(order_status=order_status)
    else:
        order_db = Order.objects.all()

    all_orders = []
    for order in order_db:
        all_orders.append({
            'customer': order.customer.name,
            'order_name': order.order_name,
            'id': order.order_id,
            'date': order.date,
            'order_status': order.order_status
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
        except Order.DoesNotExist:
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
            'order_name': invoice.order.order_name,
            'invoice_amount': invoice.invoice_amount,
            'address': invoice.address,
            'date':invoice.date,
            'customer_name': invoice.customer_name,
            'invoice_status':invoice.invoice_status
        })
    return JsonResponse(all_invoices, safe=False)


@csrf_exempt
def create_invoice(request):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        order_name=data.get('order_name')
        print("I have crossed this line")
        invoice_amount=data.get('invoice_amount')
        address=data.get('address')
        invoice_status= data.get('invoice_status')
        order_obj = Order.objects.get(order_name=order_name)
        Invoice.objects.create(
            order= order_obj,
            invoice_amount=invoice_amount, 
            address=address,
            invoice_status=invoice_status
        )
        return HttpResponse()

def get_invoice(request, pk):
    order_obj = Order.objects.get(order_id=pk)
    invoice = Invoice.objects.get(order=order_obj)
    data = {
        "order_id":pk,
        "order_name":order_obj.order_name,
        "invoice_amount":invoice.invoice_amount,
        "address":invoice.address,
        "invoice_status":invoice.invoice_status
    }
    return JsonResponse(data)


@csrf_exempt
def update_invoice(request):
    print("update invoice was called")
    if request.method == 'POST':
        print("I am post methjod")
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        order_name = data.get('order_name')
        address = data.get('address')
        invoice_amount= data.get('invoice_amount')
        invoice_status= data.get('invoice_status')

        order_obj = Order.objects.get(order_name=order_name)
        invoice_obj =Invoice.objects.get(order=order_obj)
        invoice_obj.address = address
        invoice_obj.invoice_amount = invoice_amount
        invoice_obj.invoice_status = invoice_status
        invoice_obj.save()

    return HttpResponse()


@csrf_exempt
def delete_invoice(request, pk):

    if request.method == 'DELETE':
        # data = json.loads(request.body.decode('utf-8'))
        # print(data)
        # customer_id = data.get('customer_id')
        try:
            order_obj = Order.objects.get(order_id = pk)
            invoice = Invoice.objects.get(order=order_obj)
            invoice.delete()
            return JsonResponse({'message': 'Invoice deleted successfully'}, status=204)
        except Invoice.DoesNotExist:
            return JsonResponse({'error': 'Invoice not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


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

@csrf_exempt
def create_quotation(request):

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        quotation_name=data.get('quotation_name')
        supplier_name=data.get('supplier_name')
        quotation_status = data.get('quotation_status')
        
        Quotation.objects.create(
           quotation_name= quotation_name,
           supplier=Supplier.objects.get(supplier_name=supplier_name),
           quotation_status = quotation_status
        )
        return HttpResponse()

@csrf_exempt
def update_quotation(request):
    print("update quotation was called")
    if request.method == 'POST':
        print("I am post methjod")
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        quotation_id = data.get('quotation_id')
        quotation_name= data.get('quotation_name')
        quotation_status= data.get('quotation_status')

        quotation_obj =Quotation.objects.get(id=quotation_id)
        quotation_obj.quotation_name = quotation_name
        quotation_obj.quotation_status = quotation_status
        quotation_obj.save()

    return HttpResponse()

@csrf_exempt
def delete_quotation(request, pk):

    if request.method == 'DELETE':
        # data = json.loads(request.body.decode('utf-8'))
        # print(data)
        # customer_id = data.get('customer_id')
        try:
            supplier =  Quotation.objects.get(id=pk)
            supplier.delete()
            return JsonResponse({'message': 'Quotaton deleted successfully'}, status=204)
        except Quotation.DoesNotExist:
            return JsonResponse({'error': 'qotation not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_quotation(request, pk):
    quotation_obj = Quotation.objects.get(id=pk)
    data = {
        "quotation_name":quotation_obj.quotation_name,
        "supplier_name":quotation_obj.supplier.supplier_name,
        "quotation_status":quotation_obj.quotation_status
    }

    return JsonResponse(data)


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
        except Supplier.DoesNotExist:
            return JsonResponse({'error': 'Supplier not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def list_revenue(request):
    final_predict_df = get_prediction()
    final_predict_df.rename(columns={"SVM Prediction": "SVM_Prediction"}, inplace=True)
    
    # Convert 'date' column to datetime format
    final_predict_df['date'] = pd.to_datetime(final_predict_df['date'])
    # Extract month name from the 'date' column and assign it to a new column 'month'
    final_predict_df['month'] = final_predict_df['date'].dt.strftime('%b-%y')
    print(final_predict_df)
    json_data = final_predict_df.to_dict(orient='records')
    json_data = json_data[0:5]
    return JsonResponse(json_data, safe=False)

def list_demand(request):
    final_predict_dfs = get_demand()
    json_responses={}
    final_response = list()
    for key, df in final_predict_dfs.items():
        # print(df.dtype())

        json_data = df.to_dict(orient='records')
        json_responses[key]=json_data
    final_response.append(json_responses)
    return JsonResponse(final_response, safe=False)
    


def list_employees(request):
    employee_db = Employee.objects.all()
    all_employees = list ()
    for employee in employee_db:
        all_employees.append({
            'employee_id':employee.id,
            'name':employee.name,
            'address':employee.address,
            'phone_number':employee.phone_number,
            'date_of_joining':employee.date_of_joining,
        })
    return JsonResponse(all_employees, safe=False)


@csrf_exempt
def create_employees(request):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        name=data.get('name')
        address=data.get('address')
        phone_number=data.get('phone_number')
        Employee.objects.create(
            name=name,
            address=address, 
            phone_number=phone_number
        )
        return HttpResponse()




@csrf_exempt
def update_employees(request):
    print("I was called")
    if request.method == 'POST':
        print("I have passed the condition check")
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        id = data.get('id')
        name=data.get('name')
        address=data.get('address')
        phone_number=data.get('phone_number')
        employee=Employee.objects.get(id=id)
        employee.name=name
        employee.address=address
        employee.phone_number=phone_number
        employee.save()
    return HttpResponse()

def get_employees(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    data = {
        'id': employee.pk,
        'name': employee.name,
        'address': employee.address,
        'phone_number':employee.phone_number
    }
    return JsonResponse(data)

@csrf_exempt
def delete_employees(request, pk):

    if request.method == 'DELETE':
        # data = json.loads(request.body.decode('utf-8'))
        # print(data)
        # customer_id = data.get('customer_id')
        try:
            employee = Employee.objects.get(id=pk)
            employee.delete()
            return JsonResponse({'message': 'Employee deleted successfully'}, status=204)
        except Supplier.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

def list_salary(request):
    salary_db = Salary.objects.all()
    all_salary = list()
    for salary in salary_db:
        all_salary.append({
            'employee':salary.name.name,
            'salary_id':salary.id,
            'employee_id':salary.name.id,
            'date':salary.date,
            'amount':salary.amount
        })
    
    return JsonResponse(all_salary, safe=False)


@csrf_exempt
def create_salary(request):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        employee=data.get('employee_name')
        amount = data.get('amount')
        Salary.objects.create(
            employee=Employee.objects.get(name=employee),
            salary_amount=amount
        )
        return HttpResponse()

def get_salary(request, employee_id):
    employee_obj = Employee.objects.get(id=employee_id)
    employee_name = employee_obj.name
    salary_objs = Salary.objects.filter(name=employee_obj)
    print("These are salary objs",salary_objs)
    all_data = []
    for salary_obj in salary_objs:
        all_data.append({
            "salary_id":salary_obj.id,
            "employee_id":employee_id,
            "employee_name":employee_name,
            "date":salary_obj.date,
            "amount":salary_obj.amount
        })

    return JsonResponse(all_data, safe=False) 

from django.db.models import Sum
@csrf_exempt
def get_monthly_salary(request,employee_id,month):
# if request.method == 'POST':
#     print("I am post methjod")
#     data = json.loads(request.body.decode('utf-8'))
#     print(data)
#     employee_id = data.get('employee_id')
#     month= data.get('month')
    # Assuming your Salary model has fields 'employee_name', 'date', and 'amount'
    # 'date' field represents the date of the salary
    # 'amount' field represents the salary amount
    month_mapping = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    employee_obj = Employee.objects.get(id=employee_id)
    # Filter salaries by employee name and month
    monthly_salaries = Salary.objects.filter(
        name=employee_obj,
        date__month=month_mapping[month]
    )

    # Calculate the sum of salaries for the month
    total_salary_for_month = monthly_salaries.aggregate(total_salary=Sum('amount'))['total_salary']
    final_output = list()
    data = {
        "employee_name": employee_obj.name,
        "month": month,
        "salary":total_salary_for_month
    }
    final_output.append(data)
    # Return the total salary as JSON response
    return JsonResponse(final_output , safe=False)


from django.db.models import Sum
@csrf_exempt
def get_annual_salary(request,employee_id):
# if request.method == 'POST':
#     print("I am post methjod")
#     data = json.loads(request.body.decode('utf-8'))
#     print(data)
#     employee_id = data.get('employee_id')
#     month= data.get('month')
    # Assuming your Salary model has fields 'employee_name', 'date', and 'amount'
    # 'date' field represents the date of the salary
    # 'amount' field represents the salary amount
    employee_obj = Employee.objects.get(id=employee_id)
    # Filter salaries by employee name and month
    employee_salaries = Salary.objects.filter(
        name=employee_obj
    )

    # Calculate the sum of salaries for the month
    annual_salary = employee_salaries.aggregate(total_salary=Sum('amount'))['total_salary']
    final_output = list()
    data = {
        "employee_name": employee_obj.name,
        "annual_salary":annual_salary
    }
    final_output.append(data)
    # Return the total salary as JSON response
    return JsonResponse(final_output , safe=False)

from calendar import month_abbr
def get_monthly_salary_by_year(request, employee_id, year):
    employee_obj = Employee.objects.get(id=employee_id)
    yearly_data = []

    # Iterate over all months in the year
    for month_number in range(1, 13):
        # Filter salaries by employee name, year, and month
        monthly_salaries = Salary.objects.filter(
            name=employee_obj,
            date__year=year,
            date__month=month_number
        )

        # Calculate the sum of salaries for the month
        total_salary_for_month = monthly_salaries.aggregate(total_salary=Sum('amount'))['total_salary']

        # Set total_salary_for_month to 0 if it's None (no records found for the month)
        if total_salary_for_month is None:
            total_salary_for_month = 0

        # Append the data for the month to the yearly_data list
        yearly_data.append({
            'month': month_abbr[month_number],
            'salary': total_salary_for_month
        })

    # Return the yearly data as JSON response
    return JsonResponse(yearly_data, safe=False)


@csrf_exempt
def update_salary(request):
    print("update order was called")
    if request.method == 'POST':
        print("I am post methjod")
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        salary_id = data.get('salary_id')
        amount= data.get('amount')

        salary_obj =Salary.objects.get(salary_id=salary_id)
        salary_obj.amount = amount
        salary_obj.save()

    return HttpResponse()


@csrf_exempt
def delete_salary(request, pk):

    if request.method == 'DELETE':
        # data = json.loads(request.body.decode('utf-8'))
        # print(data)
        # customer_id = data.get('customer_id')
        try:
            salary = Salary.objects.get(salary_id=pk)
            salary.delete()
            return JsonResponse({'message': 'Order deleted successfully'}, status=204)
        except Salary.DoesNotExist:
            return JsonResponse({'error': 'order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    



def calculate_salary( employee_id):
    # Retrieve the employee
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee does not exist'})

    # Retrieve today's attendance record for the employee
    today = datetime.now().date()
    try:
        attendance_today = Attendance.objects.get(employee=employee, check_in__date=today)
    except Attendance.DoesNotExist:
        return JsonResponse({'error': 'Employee has not checked in today'})

    # Check if employee has checked out
    if attendance_today.check_out is None:
        return JsonResponse({'error': 'Employee has not checked out yet'})

    # Calculate total hours worked for the day
    hours_worked = (attendance_today.check_out - attendance_today.check_in).total_seconds() / 3600

    # Calculate years of experience
    years_of_experience = (datetime.now().date() - employee.date_of_joining) // timedelta(days=365)
    print("This is the years of experience", years_of_experience)
    # Set default salary based on years of experience
    if years_of_experience >= 5:
        default_salary = 200
    else:
        default_salary = 100

    # Assuming salary is constant for all employees
    daily_salary = default_salary

    # Calculate salary for the day
    salary = daily_salary
    if hours_worked < 8:
        salary /= 2

    # Check if a Salary instance already exists for today's date and the employee
    existing_salary = Salary.objects.filter(Q(name=employee) & Q(date=today)).first()

    if existing_salary:
        return JsonResponse({'error': 'Salary already exists for today'})

    # Create a new salary instance
    Salary.objects.create(name=employee, amount=salary, date=today)

    return JsonResponse({'employee': employee.name, 'hours_worked': hours_worked, 'salary': salary})




@csrf_exempt
def mark_attendance(request):
    # list of employees will be passed later rather than a single employee's ID so remember that

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        action = data.get('action')
        employee_ids = data.get('employee_ids', [])
        if action not in ['check_in', 'check_out']:
            print( 'Invalid action')
        for employee_id in employee_ids:
            try:
                employee = Employee.objects.get(id=employee_id)
            except Employee.DoesNotExist:
                print ('Employee does not exist')

            # Retrieve today's attendance record for the employee
            today = datetime.now().date()
            try:
                attendance_today = Attendance.objects.get(employee=employee, check_in__date=today)
                    # Update check-out time if action is check_out
                if action == 'check_in':
                    print("Bro has already checked in", employee.name)
                    break
                if action == 'check_out' and attendance_today.check_out is None:
                    print("This is today when checkout is clicked", today)
                    attendance_today.check_out = datetime.now()
                    print("This is checkin time",attendance_today.check_in)
                    print("This is checkout time",attendance_today.check_out)
                    attendance_today.save()
                    calculate_salary(employee_id=employee_id)
                    print('Checked out successfully', employee.name)
                elif action == 'check_out' and attendance_today.check_out is not None:
                    print("Bro has checkout already", employee.name)
            except Attendance.DoesNotExist:
                # If the employee has not checked in today, create a new attendance record for check-in
                if action == 'check_in':
                    print("This is today when checkin is clicked", today)
                    Attendance.objects.create(employee=employee)
                    print( 'Checked in successfully', employee.name)
                elif action == 'check_out':
                    print('Employee has not checked in today')
            # If the employee has already checked out today, return error
            # if action == 'check_in' and attendance_today.check_out is not None:
            #     print( 'Employee has already checked out for today')

            
    
    else:
        print("Invalid request method")
    
    return HttpResponse()




def list_attendance(request):
    attendance_db = Attendance.objects.all()
    all_attendance = list()
    for attendance in attendance_db:
        all_attendance.append({
            'attendance_id': attendance.id,
            'employee':attendance.employee.name,
            'check_in':attendance.check_in,
            'check_out':attendance.check_out
        })
    
    return JsonResponse(all_attendance, safe=False)


def get_attendance(request, employee_id):
    employee_obj = Employee.objects.get(id=employee_id)
    employee_name = employee_obj.name
    attendance_objs = Attendance.objects.filter(employee=employee_obj)
    all_data = []
    for attendance_obj in attendance_objs:

        check_in = str(attendance_obj.check_in)
        # Parse the timestamp string into a datetime object
        timestamp = datetime.fromisoformat(check_in.replace('Z', '+00:00'))
        # Convert the datetime object to the desired time format
        check_in_time = timestamp.strftime("%I:%M %p")

        check_out = str(attendance_obj.check_out)
        # Parse the timestamp string into a datetime object
        timestamp = datetime.fromisoformat(check_out.replace('Z', '+00:00'))
        # Convert the datetime object to the desired time format
        check_out_time = timestamp.strftime("%I:%M %p")

        all_data.append({
            # "attendance_id":attendance_obj.id,
            # "employee_id":employee_id,
            "employee_name":employee_name,
            "date":attendance_obj.check_in.date(),
            "check_in_time": check_in_time,
            "check_out_time": check_out_time,
            "check_in":attendance_obj.check_in,
            "check_out":attendance_obj.check_out
        })

    return JsonResponse(all_data, safe=False)



def give_estimated_materials(request):
    raw_materials_prices= {
    "Junction Box (S)" : 450, 
    "MS Brackets" : 150, 
    "MS PLatform" : 1250, 
    "Sheet Metal Boxes" : 100, 
    "Square Sheet Metal Junction Box" : 1000
    }

    HOLDING_COST = 100

    def calculate_eoq(H,D,S):
        Q = math.sqrt(2*D*S /H)
        print("Mai KYU HU",Q)
        return Q
    
    response = list_demand(request)
    json_data_bytes = response.content
    json_data_str = json_data_bytes.decode('utf-8')
    data = json.loads(json_data_str)
    # print("This is json_data", data[0]['MS Brackets'])

    Junction_Box_pred = data[0]['Junction Box (S)'][0]['SVM Prediction']
    MS_Brackets_pred = data[0]['MS Brackets'][0]['SVM Prediction']
    MS_PLatform_pred = data[0]['MS PLatform'][0]['SVM Prediction']
    Sheet_Metal_Boxes_pred = data[0]['Sheet Metal Boxes'][0]['SVM Prediction']
    Square_Sheet_Metal_Junction_Box_pred = data[0]['Square Sheet Metal Junction Box'][0]['SVM Prediction']
    print("I am Sheet metal boxes pred", Sheet_Metal_Boxes_pred)
    
    estimated_units =[
        {
            "mat_id":"1",
            "mat_name":"MS_Brackets",
            "units": math.ceil(calculate_eoq(H=HOLDING_COST,D=MS_Brackets_pred,S=raw_materials_prices['MS Brackets'])),
        },
    # "MS_Brackets": math.ceil(calculate_eoq(H=HOLDING_COST,D=MS_Brackets_pred,S=raw_materials_prices['MS Brackets'])),
        {
            "mat_id":"2",
            "mat_name":"Square_Sheet_Metal_Junction_Box",
            "units": math.ceil(calculate_eoq(H=HOLDING_COST,D=Square_Sheet_Metal_Junction_Box_pred,S=raw_materials_prices['Square Sheet Metal Junction Box'])),
        },
    # "Square_Sheet_Metal_Junction_Box": math.ceil(calculate_eoq(H=HOLDING_COST,D=Square_Sheet_Metal_Junction_Box_pred,S=raw_materials_prices['Square Sheet Metal Junction Box'])),
        {
            "mat_id":"3",
            "mat_name":"Sheet_Metal_Boxes",
            "units": math.ceil(calculate_eoq(H=HOLDING_COST,D=Sheet_Metal_Boxes_pred,S=raw_materials_prices['Sheet Metal Boxes'])),
        },
        # "Sheet_Metal_Boxes": math.ceil(calculate_eoq(H=HOLDING_COST,D=Sheet_Metal_Boxes_pred,S=raw_materials_prices['Sheet Metal Boxes'])),
        {
            "mat_id":"4",
            "mat_name":"Junction_Box",
            "units": math.ceil(calculate_eoq(H=HOLDING_COST,D=Junction_Box_pred,S=raw_materials_prices['Junction Box (S)'])),
        },
        # "Junction_Box": math.ceil(calculate_eoq(H=HOLDING_COST,D=Junction_Box_pred,S=raw_materials_prices['Junction Box (S)'])),
        {
            "mat_id":"5",
            "mat_name":"MS_PLatform",
            "units": math.ceil(calculate_eoq(H=HOLDING_COST,D=MS_PLatform_pred,S=raw_materials_prices['MS PLatform'])),
        }
    # "MS_PLatform": math.ceil(calculate_eoq(H=HOLDING_COST,D=MS_PLatform_pred,S=raw_materials_prices['MS PLatform'])),

    ]
    print("I am the life", estimated_units)
    # final_data= list()
    # final_data.append(estimated_units)
    return JsonResponse(estimated_units, safe=False)