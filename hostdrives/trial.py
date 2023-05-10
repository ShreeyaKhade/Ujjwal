from django.shortcuts import render,HttpResponseRedirect,redirect
from . import models
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import websiteUser
# Create your views here.
from django.urls import reverse
from datetime import datetime
from django.core.mail import send_mail

def join(request,id):
    print(id)
    currDrive=models.drive.objects.get(id=id)
    currUser=websiteUser.objects.filter(user=request.user)
    currDrive.attendees.add(currUser[0])
    
    prevHosted=currUser[0].attended
    models.websiteUser.objects.filter(user=request.user).update(attended=prevHosted+1)
    send_email(request,id)

def send_email(request,id):
   htmly=get_template('') 
   d = {'first_name':request.user.name, 'id':request.drive.name}
   subject, from_email, to_email= 'Joined Successfully!', EMAIL_HOST_USER, "sanketkittad02@gmail.com"

