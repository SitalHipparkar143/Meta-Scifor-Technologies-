from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from .models import Employee


# Create your views here.
def index(request):
    return render(request,'index.html')

def all_emp(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees
    }
    print(context)
    return render(request,'view_all_emp.html',context)

def add_emp(request):
    if request.method=='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        phone = int(request.POST['phone'])
        hire_date =request.POST['hire_date']

        new_emp = Employee(first_name=first_name,last_name=last_name,salary=salary,bonus=bonus,dept_id=dept,role_id=role,phone=phone, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse('Employee added Successfully!!!')
    elif request.method=='GET':
        return render(request, 'add_emp.html')
    else:
        return render(request,'An Exception Occurred!! Employee has not been Added')

def remove_emp(request, emp_id = 0 ):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id = emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed successfully!!!")
        except ValueError:
            return HttpResponse("Please Enter A Valid Emp Id")

    employees = Employee.objects.all()
    context = {
        'employees': employees
    }
    return render(request,'remove_emp.html',context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        employees = Employee.objects.all()
        if name:
            employees = employees.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            employees = employees.filter(dept__name__icontains = dept)
        if role:
            employees = employees.filter(role__name__icontains = role)

        context ={
            'employees': employees
        }
        return render(request, 'view_all_emp.html',context)
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred!!')





