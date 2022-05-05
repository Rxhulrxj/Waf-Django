from turtle import st
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from collections import Counter
from urllib.parse import urlparse
from random import sample
from subprocess import run, PIPE
import requests.exceptions
import requests
import argparse
# import operator
import sys
import time
from . import waf
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
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                return redirect('login')
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

        context = {}
        return render(request, 'accounts/log-in.html', context)


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

