from django.shortcuts import render,HttpResponseRedirect,redirect
from . import models
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import websiteUser
# Create your views here.
from django.urls import reverse

joinRecvd=False
joinMessage=""
joinType=""
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
        newDrive=models.drive(name=name,location=location,description=description,date=date,organizer=request.user)
        newDrive.save()
        userinfo=models.websiteUser.objects.filter(user=request.user)
        prevHosted=userinfo[0].hosted
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
        return redirect('joinlist',{})
    return redirect('loginform')
@login_required(redirect_field_name='login')
def joinlist(request):
    driveset=models.drive.objects.all()
    userinfo=models.websiteUser.objects.get(user=request.user)
    global joinRecvd
    global joinMessage
    global joinType
    return render(request,"hostdrives/joinlist.html",{"drives": driveset,"userinfo":userinfo,"joinRcvd":joinRecvd,"joinMessage":joinMessage,"joinType":joinType})      
def join(request,id):
    print(id)
    currDrive=models.drive.objects.get(id=id)

    currDrive.attendees.add(request.user)
    userinfo=models.websiteUser.objects.filter(user=request.user)
    prevHosted=userinfo[0].attended
    models.websiteUser.objects.filter(user=request.user).update(attended=prevHosted+1)
    global joinRecvd
    global joinMessage
    global joinType
    joinRecvd=True
    joinMessage=currDrive.name+" Joined succesfully!"
    joinType="success"
    return redirect('joinlist')
def withdraw(request,id):
    currDrive=models.drive.objects.get(id=id)

    currDrive.attendees.remove(request.user)
    userinfo=models.websiteUser.objects.filter(user=request.user)
    prevHosted=userinfo[0].attended
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
    redirect('home')
def logout(request):
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