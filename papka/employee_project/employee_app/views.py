

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
# Create your views here.

def employee(request):
    employees = Employees.objects.all()
    positions = Position.objects.all()
    search_name = request.GET.get('search_name')
    if search_name:
        employees = employees.filter(employee_fio__icontains=search_name)

    filter_position = request.GET.get('filter_position', '')
    if filter_position:
        employees = employees.filter(position_id = filter_position)

    context = {
        'employees': employees,
        'positions': positions,
        'search_name': search_name,
        'filter_position': filter_position
    }
    return render(request, 'employee.html', context)

def auth_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username, password)

        if user.groups.filter(name='admin').exists():
            login(request, user)
            return redirect('employee')
        elif user.groups.filter(name='manager').exists():
            login(request, user)
            return redirect('employee')


    return render(request, 'auth.html')

def logout_view(request):
    logout(request)
    return redirect('auth')

def register_view(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = User.objects.create_user(username, password)
        group = Group.objects.get(id = role)
        user.groups.add(group)

        login(request, user)
        return redirect('employee')
    return render(request, 'register.html', {
        'groups': groups
    })

def edit_view(request, empl_id):
    companies = Companies.objects.all()
    positions = Position.objects.all()
    employee = Employees.objects.get(id=empl_id)

    if request.method == 'POST':
        employee.employee_fio = request.POST.get('fio')
        employee.passport_series = request.POST.get('passport_series')
        employee.passport_number = request.POST.get('passport_number')
        employee.address = request.POST.get('address')
        compane_name_id = request.POST.get('compane_name_id')
        position_id = request.POST.get('position_id')
        employee.start_date = request.POST.get('start_date')

        employee.compane_name = Companies.objects.get(id = compane_name_id)
        employee.position = Position.objects.get(id = position_id)

        employee.save()

        return redirect('employee')
    return render(request, 'edit.html', {
        'companies': companies,
        'positions': positions,
        'employee': employee
    })

def add_view(request):
    companies = Companies.objects.all()
    positions = Position.objects.all()
    if request.method == 'POST':
        employee_fio = request.POST.get('fio')
        passport_series = request.POST.get('passport_series')
        passport_number = request.POST.get('passport_number')
        address = request.POST.get('address')
        compane_name_id = request.POST.get('compane_name_id')
        position_id = request.POST.get('position_id')
        start_date = request.POST.get('start_date')

        compane_name = Companies.objects.get(id = compane_name_id)
        position = Position.objects.get(id = position_id)

        Employees.objects.create(
            employee_fio = employee_fio,
            passport_series = passport_series,
            passport_number = passport_number,
            address = address,
            compane_name = compane_name,
            position = position,
            start_date = start_date
        )
        return redirect('employee')
    return render(request, 'add.html', {
        'companies': companies,
        'positions': positions,
    })

def delete_view(request, empl_id):
    employee = get_object_or_404(Employees, id=empl_id)
    employee.delete()
    return redirect('employee')