from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib import messages

from .models import Customer,Service
from login_app.models import Employee


#  Add new Customer
def new(request):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        context={
            'user':user
        }
    return render(request,"addcust.html",context)

def add(request):
    if ('employeeid' in request.session) :
        errors = Customer.objects.customer_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/crm/new')
        else:
            Customer.objects.create(first_name=request.POST['first'],last_name=request.POST['last'],
            city=request.POST['city'],speed=request.POST['speed'])
            return redirect('/crm/all_customers')
    else:
        return redirect('/')

#Search for a customer
def search(request):
    if ('employeeid' in request.session) :
        request.session['search'] = request.POST['search']
        return redirect('/crm/search/result')
    else:
        return redirect('/')

def result(request):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
    cust1 = list(Customer.objects.filter(
        first_name__contains=request.session['search']))
    cust2 = list(Customer.objects.filter(
        last_name__contains=request.session['search']))
    cust3 = list(Customer.objects.filter(
        city__contains=request.session['search']))
    cust = list(set(cust1+cust2+cust3))
    context = {
        'cust': cust,
        'user':user
    }
    return render(request, 'result.html', context)

# Serch for a user
def search_user(request):
    if ('employeeid' in request.session) :
        request.session['search'] = request.POST['search']
        return redirect('/crm/search/user_result')
    else:
        return redirect('/')

def user_reuslt(request):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
    user1 = list(Employee.objects.filter(
        first_name__contains=request.session['search']))
    user2 = list(Employee.objects.filter(
        last_name__contains=request.session['search']))
    user3 = list(Employee.objects.filter(
        email__contains=request.session['search']))
    users = list(set(user1+user2+user3))
    context = {
        'users': users,
        'user':user
    }
    return render(request, 'user_result.html', context)

# Get all customers
def all_customers(request):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        customers=Customer.objects.all()
        context={
            'all_custemors':customers,
            'user':user,
        }
    return render(request,"all_customers.html",context)

# Update a customer update_customer
def edit_customer(request, cust_id):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        context = {
            'user':user,
            'this_cust': Customer.objects.get(id=cust_id),
            }
        return render(request, 'edit_cust.html', context)
    else:
        return redirect('/crm/all_customers')


def update_cust(request, this_cust_id):
    if ('employeeid' in request.session) :
        errors = Customer.objects.customer_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/crm/edit_cust/{this_cust_id}')
        else:
            this_cust = Customer.objects.get(id=this_cust_id)
            this_cust.first_name = request.POST['first']
            this_cust.last_name = request.POST['last']
            this_cust.city = request.POST['city']
            this_cust.speed = request.POST['speed']
            this_cust.save()
            return redirect('/crm/all_customers')
    else:
        return redirect('/')

# Delete a customer
def delete_customer(request, user_id):
    if ('employeeid' in request.session) :
        this_customer = Customer.objects.get(id=user_id)
        this_customer.delete()
        return redirect('/crm/all_customers') 
    else:
        return redirect('/')

# Viewing customer details
def customer_details(request, c_id):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        this_customer=Customer.objects.get(id=c_id)
        all_services=Service.objects.all()
        context={
            "this_customer":this_customer,
            "user":user,
            'all_services':all_services
            }
        return render (request,"cust_details.html",context)  
    else:
        return redirect("/") 

# Add new Service
def new_service(request):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        if user.admin:
            context={
                'user':user
            }
            return render(request,"add_serv.html",context)
        else:
            return redirect('/crm/all_services')


def add_service(request):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        if user.admin:
            errors = Service.objects.service_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/crm/new_service')
            else:
                Service.objects.create(name=request.POST['name'],price=request.POST['price'])
                return redirect('/crm/all_services')
        else:
            return redirect('/crm/all_services')
    else:
        return redirect('/')  

# Get all Services
def all_services(request):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        services=Service.objects.all()
        context={
            'all_services':services,
            'user':user,
        }
    return render(request,"services.html",context)

# Update a service
def edit_serv(request, serv_id):
    user = Employee.objects.get(id=request.session['employeeid'])
    if user.admin:
        context = {
            'user':user,
            'this_serv': Service.objects.get(id=serv_id),
        }
        return render(request, 'edit_serv.html', context)
    else:
        return redirect('/crm/all_services')


def update_serv(request, this_serv_id):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        if user.admin:
            errors = Service.objects.service_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/crm/edit_serv/{this_serv_id}')
            else:
                this_serv = Service.objects.get(id=this_serv_id)
                this_serv.name = request.POST['serv']
                this_serv.price = request.POST['price']
                this_serv.save()
                return redirect('/crm/all_services')
        else:
            return redirect('/crm/all_services')
    else:
        return redirect('/')

# Delete a service
def delete_serv(request, serv_id):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        if user.admin:
            serv = Service.objects.get(id=serv_id)
            serv.delete()
            return redirect('/crm/all_services')
        else:
            return redirect('/crm/all_services')
    else:
        return redirect('/')

# Search for service
def search_serv(request):
    if ('employeeid' in request.session) :
        request.session['search'] = request.POST['search']
        return redirect('/crm/search/serv_result')
    else:
        return redirect('/')

def serv_reuslt(request):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
    service = list(Service.objects.filter(
        name__contains=request.session['search']))
    
    serv = list(set(service))
    context = {
        'serv': serv,
        'user':user
    }
    return render(request, 'serv_result.html', context)

# Offers page
def offers(request):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        context={
            'user':user
        }
    return render(request,'offers.html',context)


def customer_services(request, cust_id):
    if ('employeeid' in request.session):
        user = Employee.objects.get(id=request.session['employeeid'])
        this_cust = Customer.objects.get(id=cust_id)
        available_services = Service.objects.exclude(customers=cust_id)
        context = {
            'user': user,
            'this_cust': this_cust,
            'customer_services': this_cust.services.all(),
            'available_services': available_services,
        }
        return render(request, 'cust_serv.html', context)
    else:
        return redirect('/')

# Add a service to customer
def add_service_to_cust(request, cust_id, serv_id):
    if ('employeeid' in request.session):
        this_cust = Customer.objects.get(id=cust_id)
        this_serv = Service.objects.get(id=serv_id)
        this_cust.services.add(this_serv)
        return redirect(f'/crm/cust_serv/{cust_id}')
    else:
        return redirect('/')

# Remove a service from a customer
def delete_service_from_cust(request, cust_id, serv_id):
    if ('employeeid' in request.session):
        this_cust = Customer.objects.get(id=cust_id)
        this_serv = Service.objects.get(id=serv_id)
        this_cust.services.remove(this_serv)
        return redirect(f'/crm/cust_serv/{cust_id}')
    else:
        return redirect('/')
