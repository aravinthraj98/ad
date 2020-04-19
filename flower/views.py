from django.shortcuts import render,redirect
from django.http import HttpResponse
from flower.models import signup
from shop.models import product



def dataadmin(request):
    return render(request,'flower/admin.html')

def signin(request):
        return render(request,'flower/signin.html',{'page':'SIGNUP NOW'})
def signin_v(request):
    if request.method =="POST":
        user=request.POST['uname']
        pwd=request.POST['pass']
        cpwd=request.POST['cpass']
        mail=request.POST['email']
        if signup.objects.filter(username=user,email=mail).exists():
               return render(request,'flower/signin.html',{'msg':'username or mail exist','page':'SIGNUP NOW'})
        else:
            if(pwd==cpwd):
                   signup.objects.create(username=user,password=pwd,email=mail)
                   return render(request,'flower/login.html',{'msg':'registeredsuccessfully'})
            else:
                   return render(request,'flower/signin.html',{'msg':'password mismatch','uname':request.POST['uname'],'page':'SIGNUP NOW'})

    else:
        return HttpResponse("unable to process ur request")

def login_v(request):
    if request.method =='POST':
        user=request.POST['uname']
        pwd=request.POST['pass']
        if signup.objects.filter(username=user,password=pwd).exists():
             t=product.objects.all()
             request.session['user']=user
             return redirect('/show')

        else:
               return render(request,'flower/login.html',{'msg':'username or password mismatch'})
    else:
        return render(request,'flower/login.html')

def reset(request):
    return render(request,'flower/reset.html',{'page':'RESET UR PASSWORD'})
def resv(request):
    if request.method=="POST":
        user=request.POST['uname']
        pwd=request.POST['pass']
        cpwd=request.POST['cpass']
        mail=request.POST['email']
        if signup.objects.filter(username=user,email=mail):
            if(pwd==cpwd):
                signup.objects.filter(username=user).update(password=pwd)
                return render(request,'flower/login.html',{'msg':'password reset successfully','page':"LOGIN"})
            else:
                return render(request,'flower/reset.html',{'msg':'password mismatch','page':'RESET UR PASSWORD'})
        else:
                return render(request,'flower/reset.html',{'msg':'username or email id mismatch','page':'RESET UR PASSWORD'})
    

# Create your views here.
