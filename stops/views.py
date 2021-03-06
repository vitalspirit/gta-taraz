
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout






def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'New user ' + user + ' registered successfully')
            return redirect('stops:login')
    context={'form': form}
    return render(request, 'stops/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('stops:index')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'stops/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('stops:login')




@login_required(login_url='stops:login')
def index(request):
    return render(request, 'stops/dashboard.html')

@login_required(login_url='stops:login')
def shutdowns(request):
    all_shutdowns = Shutdown.objects.order_by('-datetime')
    return render(request, 'stops/shutdowns.html', {'all_shutdowns': all_shutdowns})

@login_required(login_url='stops:login')
def gtu_info(request):
    return render(request, 'stops/gtu_info.html')


@login_required(login_url='stops:login')
def shutdowns_general(request):
    return render(request, 'stops/shutdowns_general.html')

@login_required(login_url='stops:login')
def shutdowns_general_request(request):
    year  = request.POST['year']

    cs_4  = Station.objects.get(name = "CS-4")
    ccs_4 = Station.objects.get(name = "CCS-4")
    ccs_3 = Station.objects.get(name = "CCS-3")
    ccs_5 = Station.objects.get(name = "CCS-5")

    cs_4_sd_list = cs_4.shutdown_set.all().filter(datetime__year = year).order_by('-datetime')#All registered SDs
    cs_4_sd_count_year = cs_4.shutdown_set.all().filter(datetime__year = year).count()

    ccs_4_sd_list = ccs_4.shutdown_set.all().filter(datetime__year = year) #All registered SDs
    ccs_4_sd_count_year = ccs_4.shutdown_set.all().filter(datetime__year = year).count()

    ccs_3_sd_list = ccs_3.shutdown_set.all().filter(datetime__year = year) #All registered SDs
    ccs_3_sd_count_year = ccs_3.shutdown_set.all().filter(datetime__year = year).count()

    ccs_5_sd_list = ccs_5.shutdown_set.all().filter(datetime__year = year) #All registered SDs
    ccs_5_sd_count_year = ccs_5.shutdown_set.all().filter(datetime__year = year).count()

    return render(request, 'stops/shutdowns_general.html',
                    {'year': year,
                    'cs_4_sd_count_year':cs_4_sd_count_year,
                    'ccs_4_sd_count_year':ccs_4_sd_count_year,
                    'ccs_3_sd_count_year':ccs_3_sd_count_year,
                    'ccs_5_sd_count_year':ccs_5_sd_count_year,
                    'cs_4_sd_list': cs_4_sd_list,
                    'ccs_4_sd_list': ccs_4_sd_list,
                    'ccs_3_sd_list': ccs_3_sd_list,
                    'ccs_5_sd_list': ccs_5_sd_list

                    })

@login_required(login_url='stops:login')
def working_hours(request):

    cs_4_hours = W_hours.objects.all().filter(station = Station.objects.get(name = "CS-4"))
    ccs_4_hours = W_hours.objects.all().filter(station = Station.objects.get(name = "CCS-4"))
    ccs_3_hours = W_hours.objects.all().filter(station = Station.objects.get(name = "CCS-3"))
    ccs_5_hours = W_hours.objects.all().filter(station = Station.objects.get(name = "CCS-5"))
    cs_4_2018_total = cs_4_hours.filter(year = '2018').aggregate(Sum('w_hours'))
    cs_4_2019_total = cs_4_hours.filter(year = '2019').aggregate(Sum('w_hours'))
    ccs_4_2018_total = ccs_4_hours.filter(year = '2018').aggregate(Sum('w_hours'))
    ccs_4_2019_total = ccs_4_hours.filter(year = '2019').aggregate(Sum('w_hours'))
    ccs_3_2018_total = ccs_3_hours.filter(year = '2018').aggregate(Sum('w_hours'))
    ccs_3_2019_total = ccs_3_hours.filter(year = '2019').aggregate(Sum('w_hours'))
    ccs_5_2018_total = ccs_5_hours.filter(year = '2018').aggregate(Sum('w_hours'))
    ccs_5_2019_total = ccs_5_hours.filter(year = '2019').aggregate(Sum('w_hours'))
    return render(request, 'stops/hours.html',
                    {'cs_4_hours': cs_4_hours,
                    'ccs_4_hours': ccs_4_hours,
                    'ccs_3_hours': ccs_3_hours,
                    'ccs_5_hours': ccs_5_hours,
                    'cs_4_2018_total':cs_4_2018_total,
                    'cs_4_2019_total':cs_4_2019_total,
                    'ccs_4_2018_total':ccs_4_2018_total,
                    'ccs_4_2019_total':ccs_4_2019_total,
                    'ccs_3_2018_total':ccs_3_2018_total,
                    'ccs_3_2019_total':ccs_3_2019_total,
                    'ccs_5_2018_total':ccs_5_2018_total,
                    'ccs_5_2019_total':ccs_5_2019_total,
                    })


def upload_SD(request):
    if request.method == 'POST':
        form = SD_add_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('stops:shutdowns_general')
    else:
        form = SD_add_form()
    return render(request, 'stops/upload_SD.html', {'form': form})
