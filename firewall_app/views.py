from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from . import waf
from django.forms.utils import ErrorList
#  Create your views here.


def home(request):
    return render(request, 'index.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            emailvalue= request.POST.get("email")
            emailverify=User.objects.filter(email=emailvalue)
            if form.is_valid():
                if len(emailverify) == 0:
                    form.save()
                    return redirect('login')
                else:
                    form.add_error("email","Email Already Exists")  
        context = {'form': form}
        return render(request, 'accounts/sign-up.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        return render(request, 'accounts/log-in.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def checker(request):
    final_res=""
    successful_responses=""
    failure_response=""
    no_responses=""
    no_of_requests=""
    up_or_down=""
    net_issue=""
    urlinp, types, posts, useragents,out = '', 'all', '', '',''
    if request.method == 'POST':
        urlinp = request.POST.get('urlinput')
        payloadtype = request.POST.get('payloadselect')
    if urlinp != '':
        url = urlinp
        types = payloadtype
        x = waf.mainfun(url, posts, types, useragents)
        final_res,up_or_down,net_issue,successful,failure,no_of_response,no_of_request=x
        successful_responses=str(successful)
        failure_response=str(failure)
        no_responses=str(no_of_response)
        no_of_requests=str(no_of_request)
    return render(request, 'checker.html',{"final_result":final_res,"successfulresponse":successful_responses,"failureresponses":failure_response,"noresponse":no_responses,"noofrequest":no_of_requests,"upordown":up_or_down,"netissue":net_issue,"urlsent":urlinp,"paloadsent":types})

