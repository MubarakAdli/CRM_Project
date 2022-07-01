from django.shortcuts import render, redirect
from .models import Employee
from crm_app .models import Customer
from django.contrib import messages
import bcrypt


def form(request):
    if 'employeeid' in request.session:
        return redirect('/crm/all_customers')
    else:
        return render(request, 'form.html')

def register(request):
    errors = Employee.objects.register_validator(request.POST)
    request.session['which_form'] = request.POST['which_form']
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/')
    else:
        employees = Employee.objects.all()
        if len(employees) == 0:
            isAdmin = True
        else:
            isAdmin = False
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()

        Employee.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST['last_name'], 
            email=request.POST['email'], password=pw_hash, admin=isAdmin)
        employee = Employee.objects.filter(email=request.POST['email'])
        if employee:
            logged_employee = employee[0]
            request.session['employeeid'] = logged_employee.id
        return redirect('/crm/all_customers')


def login(request):
    errors = Employee.objects.login_validator(request.POST)
    request.session['which_form'] = request.POST['which_form']
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/')
    employee = Employee.objects.filter(email=request.POST['email'])
    if len(employee) != 0:
        logged_employee = employee[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_employee.password.encode()):
            request.session['employeeid'] = logged_employee.id
            return redirect('/crm/all_customers')

    return redirect('/')

def all_users(request):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        context = {
            'other_users': Employee.objects.exclude(id=user.id),
            'user':user
        }
        return render(request, 'users.html', context)
    else:
        return redirect('/')

def edit_user(request, user_id):
    user = Employee.objects.get(id=request.session['employeeid'])
    if user.admin:
        context = {
            'user':user,
            'this_user': Employee.objects.get(id=user_id)
        }
        return render(request, 'edit_user.html', context)
    else:
        return redirect('/all_employee')
    

def update_user(request, user_id):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        if user.admin:
            user_to_update = Employee.objects.get(id=user_id)
            user_to_update.email = request.POST['email']
            user_to_update.first_name = request.POST['first_name']
            user_to_update.last_name = request.POST['last_name']
            user_to_update.admin = request.POST['user_level']
            user_to_update.save()
            return redirect('/all_employee')
            
        else:
            return redirect('/users')
    else:
        return redirect('/login_form')


def delete_user(request, user_id):
    if ('employeeid' in request.session) :
        user = Employee.objects.get(id=request.session['employeeid'])
        if user.admin:
            
            user_to_delete = Employee.objects.get(id=user_id)
            user_to_delete.delete()
            return redirect('/all_employee')
        else:
            return redirect('/users')
    else:
        return redirect('/login_form')

def logout(request):
    request.session.clear()
    return redirect('/')

 