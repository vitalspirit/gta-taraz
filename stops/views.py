
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
import json




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



#@login_required(login_url='stops:login')
#def index(request):
    #return render(request, 'stops/dashboard.html')



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
    cs_4_2020_total = cs_4_hours.filter(year = '2020').aggregate(Sum('w_hours'))
    cs_4_2021_total = cs_4_hours.filter(year = '2021').aggregate(Sum('w_hours'))

    ccs_4_2018_total = ccs_4_hours.filter(year = '2018').aggregate(Sum('w_hours'))
    ccs_4_2019_total = ccs_4_hours.filter(year = '2019').aggregate(Sum('w_hours'))
    ccs_4_2020_total = ccs_4_hours.filter(year = '2020').aggregate(Sum('w_hours'))
    ccs_4_2021_total = ccs_4_hours.filter(year = '2021').aggregate(Sum('w_hours'))

    ccs_3_2018_total = ccs_3_hours.filter(year = '2018').aggregate(Sum('w_hours'))
    ccs_3_2019_total = ccs_3_hours.filter(year = '2019').aggregate(Sum('w_hours'))
    ccs_3_2020_total = ccs_3_hours.filter(year = '2020').aggregate(Sum('w_hours'))
    ccs_3_2021_total = ccs_3_hours.filter(year = '2021').aggregate(Sum('w_hours'))
    ccs_5_2018_total = ccs_5_hours.filter(year = '2018').aggregate(Sum('w_hours'))
    ccs_5_2019_total = ccs_5_hours.filter(year = '2019').aggregate(Sum('w_hours'))
    ccs_5_2020_total = ccs_5_hours.filter(year = '2020').aggregate(Sum('w_hours'))
    ccs_5_2021_total = ccs_5_hours.filter(year = '2021').aggregate(Sum('w_hours'))

    return render(request, 'stops/hours.html',
                    {'cs_4_hours': cs_4_hours,
                    'ccs_4_hours': ccs_4_hours,
                    'ccs_3_hours': ccs_3_hours,
                    'ccs_5_hours': ccs_5_hours,

                    'cs_4_2018_total':cs_4_2018_total,
                    'cs_4_2019_total':cs_4_2019_total,
                    'cs_4_2020_total':cs_4_2020_total,
                    'cs_4_2021_total':cs_4_2021_total,

                    'ccs_4_2018_total':ccs_4_2018_total,
                    'ccs_4_2019_total':ccs_4_2019_total,
                    'ccs_4_2020_total':ccs_4_2020_total,
                    'ccs_4_2021_total':ccs_4_2021_total,

                    'ccs_3_2018_total':ccs_3_2018_total,
                    'ccs_3_2019_total':ccs_3_2019_total,
                    'ccs_3_2020_total':ccs_3_2020_total,
                    'ccs_3_2021_total':ccs_3_2021_total,

                    'ccs_5_2018_total':ccs_5_2018_total,
                    'ccs_5_2019_total':ccs_5_2019_total,
                    'ccs_5_2020_total':ccs_5_2020_total,
                    'ccs_5_2021_total':ccs_5_2021_total,
                    })



@login_required(login_url='stops:login')
def upload_SD(request):
    if request.method == 'POST':
        form = SD_add_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('stops:shutdowns_general')
    else:
        form = SD_add_form()
    return render(request, 'stops/upload_SD.html', {'form': form})




@login_required(login_url='stops:login')
def index(request):

    def sub(y):
        lst=[]
        hours = W_hours.objects.filter(year = y)
        dict_cs_4={}
        dict_ccs_4={}
        dict_ccs_3={}
        dict_ccs_5={}
        for item in hours:
            if item.station == Station.objects.get(name = "CS-4"):
                dict_cs_4["category"] = item.station.name
                dict_cs_4[item.gtu] = item.w_hours
            if item.station == Station.objects.get(name = "CCS-4"):
                dict_ccs_4["category"] = item.station.name
                dict_ccs_4[item.gtu] = item.w_hours
            if item.station == Station.objects.get(name = "CCS-3"):
                dict_ccs_3["category"] = item.station.name
                dict_ccs_3[item.gtu] = item.w_hours
            if item.station == Station.objects.get(name = "CCS-5"):
                dict_ccs_5["category"] = item.station.name
                dict_ccs_5[item.gtu] = item.w_hours

        lst.append(dict_cs_4)
        lst.append(dict_ccs_4)
        lst.append(dict_ccs_3)
        lst.append(dict_ccs_5)

        app_json = json.dumps(lst)
        f = open (f"stops/templates/stops/{y}.json", "w")
        f.write(str(app_json))
        f.close()
    sub('2018')
    sub('2019')
    sub('2020')
    sub('2021')
    return render(request, 'stops/dashboard.html')
