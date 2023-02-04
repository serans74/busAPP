from .rides_functuins import all_to_city, all_from_city, check_bus_route, cities_list
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Ride, Ticket


def get_rides_plan(request):
    plan = Ride.objects.all()

    context = {'plan': plan}

    return render(request, 'all-connections.html', context)


def find_bus(request):
    cities = cities_list()
    method = 'GET'
    if request.method == 'POST':
        method = 'POST'
        first_point = request.POST.get('first_stop').strip().title()
        last_point = request.POST.get('end_stop').strip().title()
        express = request.POST.get('express')

        # taking plan for all express busses
        express_busses = Ride.objects.filter(is_express=True)

        # taking plan for all non-express busses
        standard_busses = Ride.objects.filter(is_express=False)

        # covering empty first point case
        if first_point == '':
            filtered_express_busses = [bus for bus in express_busses if all_to_city(bus, last_point)]
            filtered_standard_busses = [bus for bus in standard_busses if all_to_city(bus, last_point)]
            context = {'express_busses': filtered_express_busses,
                       'standard_busses': filtered_standard_busses,
                       'is_express': express,
                       'method': method}
            return render(request, 'home.html', context)

        # covering empty last point case
        if last_point is None or last_point == '':
            filtered_express_busses = [bus for bus in express_busses if all_from_city(bus, first_point)]
            filtered_standard_busses = [bus for bus in standard_busses if all_from_city(bus, first_point)]
            context = {'express_busses': filtered_express_busses,
                       'standard_busses': filtered_standard_busses,
                       'is_express': express,
                       'method': method}
            return render(request, 'home.html', context)

        # checking if any bus cover first and last point and if it is going in right direction
        filtered_express_busses = [bus for bus in express_busses if check_bus_route(bus, first_point, last_point)]

        # checking if any non-express bus cover first and last point and if it is going in right direction
        filtered_standard_busses = [bus for bus in standard_busses if check_bus_route(bus, first_point, last_point)]

        context = {'express_busses': filtered_express_busses,
                   'standard_busses': filtered_standard_busses,
                   'is_express': express,
                   'method': method}
        return render(request, 'home.html', context)

    context = {'method': method,
               'cities': cities}
    return render(request, 'home.html', context)


def get_single_bus(request, pk):
    bus = Ride.objects.get(id=pk)
    cities = bus.cities_where_collect_passengers.split(',')

    if request.user.is_authenticated:
        if request.method == 'POST':
            Ticket.objects.create(owner=request.user, bus=bus)
            return redirect('bus', pk)

    context = {'bus': bus,
               'cities': cities}
    return render(request, 'bus.html', context)


def registerUser(request):
    page = 'register'
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            login(request, user)
            return redirect('plan')
        else:
            messages.error(request, "An error occurred during registration")
    context = {'form': form,
               'page': page}
    return render(request, 'login-register.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        redirect('plan')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('plan')

    return render(request, 'login-register.html')


def logoutUser(request):
    logout(request)
    return redirect('plan')


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    tickets = Ticket.objects.filter(owner=user)
    price_sum = sum([ticket.bus.price for ticket in tickets])
    avg_price = price_sum / tickets.count()

    context = {'user': user,
               'tickets': tickets,
               'avg_price': avg_price,
               'price_sum': price_sum}
    return render(request, 'profile.html', context)



