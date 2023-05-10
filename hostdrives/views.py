from django.shortcuts import render,HttpResponseRedirect,redirect
from . import models
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import websiteUser
# Create your views here.
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
joinRecvd=False
joinMessage=""
joinType=""
emailmsg=""
def home(request):
   return render(request,"hostdrives/homepage.html") 
def host(request):
    
    if request.method=='POST':
        name=request.POST['driveName']
        location=request.POST['driveLocation']
        date=request.POST['driveDate']
        print(date)
        print(type(date))
        description=request.POST['driveDescription']
        currUser=websiteUser.objects.filter(user=request.user)
        newDrive=models.drive(name=name,location=location,description=description,date=date,organizer=currUser[0])
        newDrive.save()
        
        prevHosted=currUser[0].hosted
        models.websiteUser.objects.filter(user=request.user).update(hosted=prevHosted+1)
        global joinRecvd
        global joinMessage
        global joinType
        joinRecvd=False
        joinMessage=""
        joinType=""
        return redirect('joinlist')
def register(request):
    if request.method=='POST':
        #print(request.POST['name1'])
        name=request.POST['name1']
        arr=name.split(' ')
        first_name=arr[0]
        if(len(arr)>1):
            last_name=arr[1]
        else:
            last_name=""
        username=request.POST['username1']
        email=request.POST['email1']
        phoneno1=request.POST['phoneno1']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if(password1!=password2):
            return render(request,"hostdrives/loginform.html",{"exists": True,"message":"Passwords do not match"})
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() or models.websiteUser.objects.filter(phone=phoneno1).exists():
            return render(request,"hostdrives/loginform.html",{"exists": True,"message":"User already exists"})
        user=User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
        user.save()
        w=websiteUser(user=user,phone=phoneno1,hosted=0,attended=0)
        w.save()
        auth_user=authenticate(request,username=username,password=password1)
        auth_login(request,auth_user)
        return redirect('joinlist')
    return redirect('loginform')
@login_required(redirect_field_name='login')
def joinlist(request):
    #drive_rating=request.POST.get('rating')
    userinfo=models.websiteUser.objects.get(user=request.user)
    # print(driveset[0].date)
    curr=datetime.now()
    driveset=models.drive.objects.filter(date__gt=curr)
    #driveset=models.drive.objects.filter(date__gt=curr).all().order_by('-rating')
    global joinRecvd
    global joinMessage
    global joinType
    return render(request,"hostdrives/joinlist.html",{"drives": driveset,"userinfo":userinfo})      
def join(request,id):
    print(id)
    currDrive=models.drive.objects.get(id=id)
    currUser=websiteUser.objects.filter(user=request.user)
    currDrive.attendees.add(currUser[0])
    
    prevHosted=currUser[0].attended
    models.websiteUser.objects.filter(user=request.user).update(attended=prevHosted+1)
    # template='email_template.html'

    
    subject="Joined Successfully!"
    message='abc'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[request.user.email]
    send_mail(subject,message,email_from,recipient_list)
    # except BadHeaderError:
	# 	return HttpResponse('Invalid header found.')
   
    global joinRecvd
    global joinMessage
    global joinType
    joinRecvd=True
    joinMessage="joined successfully!"
    joinType="success"
    return redirect('joinlist')
def withdraw(request,id):
    currDrive=models.drive.objects.get(id=id)
    currUser=websiteUser.objects.filter(user=request.user)
    currDrive.attendees.remove(currUser[0])
    
    prevHosted=currUser[0].attended
    models.websiteUser.objects.filter(user=request.user).update(attended=prevHosted-1)
    global joinRecvd
    global joinMessage
    global joinType
    joinRecvd=True
    joinMessage=currDrive.name+" Withdrew succesfully!"
    joinType="danger"
    return redirect('joinlist')
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is None:
            return render(request,"hostdrives/loginform.html",{"exists": True})
        else:
            auth_login(request,user)
            return redirect('joinlist')
    return redirect('home')
def logout(request):
    global joinRecvd
    global joinMessage
    global joinType
    joinRecvd=False
    joinMessage=""
    joinType=""
    auth_logout(request)
    return redirect('home')
def loginform(request):
    global joinRecvd
    global joinMessage
    global joinType
    joinRecvd=False
    joinMessage=""
    joinType=""
    return render(request,"hostdrives/loginform.html",{"exists": False})

