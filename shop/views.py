from django.shortcuts import render,redirect
from django.http import HttpResponse
from shop.models import product,purchasedetail,cart as cartlist
from PIL import Image
from django import forms
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
import datetime
from datetime import date,timedelta
mydate = datetime.datetime.now()
month= mydate.strftime("%B")


productable=product.objects.all()
for i in productable:
    if i.season!=month and i.season!="all" :
        product.objects.filter(pname=i.pname).update(stockavailable="no")
DATE=date.today()
tdate=DATE-timedelta(days=2)
d=purchasedetail.objects.all()
for i in d:
    if i.date!=str(DATE):
        purchasedetail.objects.filter(orderno=i.orderno).update(status="cancelled")
    if i.date==str(tdate):
        purchasedetail.objects.filter(orderno=i.orderno).delete()


def show(request):
    if request.session['user']:
         t=product.objects.all()
         user=request.session['user']
         ordno=1
         while True:
             if cartlist.objects.filter(idno=ordno).exists():
                     ordno+=1
             else:
                    break
         if request.method == "POST":
              for i in t:
                 products=i.img
                 remove = request.POST.get(products, False);
                 if remove == "Add to Cart":
                     if cartlist.objects.filter(cname=user,pname=i.pname).exists():
                                   continue
                     
                     cartlist.objects.create(idno=ordno,cname=user,pname=i.pname,img=i.img,cost=i.cost)       
              submit = request.POST.get('filters',False)
              if submit=="applyfilter":
                  pmodel = request.POST['pmodel']
                  seasons = request.POST['season']
                  if seasons =="season":
                         season=month
                         if pmodel=="all":
                             t=product.objects.filter(season=season)
                         else:
                             t=product.objects.filter(season=season,pmodel=pmodel)
                  else:
                        if pmodel=="all":
                            t= t=product.objects.all()
                        else:
                            t=product.objects.filter(pmodel=pmodel)
                 
              
         listm=[]
         listm.append("all")
         listm.append(month)
         
         return render(request,'shop/show.html',{'detail':t,'user':user,'month':listm})
    else:
        return HttpResponse("ijnjin")
def cart(request):
      user = request.session["user"]
      t=cartlist.objects.filter(cname=user)
      if len(t)>0:
        return render(request,'shop/cart.html',{'product':t,'cart':t})
      else:
          return HttpResponse("no items in the cart")



def purchase(request):
   if request.method == "POST":
         user=request.session["user"]
     
         global list1
         list1 = []
         list2=[]
         list3=[]
         r=0
         t=cartlist.objects.filter(cname=user)
         for i in t:

             dict1={}
             
             E = request.POST[i.img]
             if  E!='0':
                 dict1["product"]=i.pname
                 dict1["quantity"]=int(E)
                 dict1["cost"]=int(E)*int(i.cost)
                 dict1["picture"]=i.img
                 r=r+dict1["cost"]
                 no="*"
                 purchaseproduct = str(i.pname)+str(no)+str(E)+"="+str(i.cost*int(E))
                 list1.append(dict1)
                 list2.append(purchaseproduct)
                 list3.append(dict1['picture'])
     
         ordno=1
         while True:
             if purchasedetail.objects.filter(orderno=ordno).exists():
                     ordno+=1
             else:
                    break
         global commitpurchase 
         commitpurchase = purchasedetail(cname=user,orderno=ordno,productdetails=list2,totalcost=r,img=list3,status='onprocess',date=str(DATE))       
         return render(request,'shop/purchase.html',{'list':list1,'totalcost':r,'user':user,'orderno':ordno})
      
   else:
          return render(request,'flower/login.html')
def confirmorder(request):
    if request.method =="POST":
        user=request.session['user']
        orderno=request.POST['orderno']
        r=0
        productlist=[]
        pimage=[]
        productname=[]
        cancel=0
        for i in list1:
            dict3={} 
            product=i["product"]
            quantity=i["quantity"]
            cost=i["cost"]
            image=i["picture"]
            remove = request.POST.get(product, False);
            
            if remove:
                cancel=1
                
            else:
               dict3['product']=product
               dict3['quantity']=quantity
               dict3['cost']=cost
               dict3['picture']=image
               r=r+cost
               productlist.append(dict3)
               no="*"
               purchaseproduct=str(product)+str(no)+str(quantity)+"="+str(cost)
               productname.append(purchaseproduct)
               pimage.append(image)
        if cancel==1:
                  global commitpurchase
                  commitpurchase = purchasedetail(cname=user,orderno=orderno,productdetails=productname,totalcost=r,img=pimage,status='onprocess',date=DATE)
        if len(productlist)==0:
            return render(request,'shop/show.html',{"noitem":"No ORDER HAS BEEN PLACED"})  
        commitpurchase.save()
        return render(request,'shop/orderconfirm.html',{'user':user,'orderno':orderno,'product':productlist,'totalcost':r})
def showorder(request):
        user=request.session['user']
        p=purchasedetail.objects.filter(cname=user)
        orderno=''
        
        for i in p:
            j="cancelorder"
            remove = request.POST.get(str(i.orderno),False)
            if remove==j:
                purchasedetail.objects.filter(orderno=i.orderno).update(status='cancelled')
                orderno="orderno"+str(i.orderno)+"hasbeencancelled"
        detail=purchasedetail.objects.filter(cname=user)

        return render(request,'shop/showorder.html',{'detail':detail,'user':user,'orderno':orderno})
              
def logout(request):
    if request.session["user"]:

      t=cartlist.objects.filter(cname=request.session["user"])
      if len(t)>0:
       for i in t:
         cartlist.objects.filter(idno=i.idno).delete()
      request.session['user']=0
      return loggedout(request)
    else:
         return HttpResponse("sjdjsd")


def loggedout(request):
        return render(request,'flower/login.html')

        

          
def updateproduct(request):
        if request.method=="POST":
            password=request.POST["pass"]
            if password =="aravinthraj":
              request.session["admin"]=1
              return render(request,'shop/update.html')
            else:
                return HttpResponse("da")
        else:
            return render(request,'shop/adminlogin.html')

def insert(request):
    if request.method == 'POST':
        pname = request.POST['pname']
        img=request.FILES['img']
        fs = FileSystemStorage()
        name=fs.save(img.name, img)
        url=fs.url(name)
        cost = request.POST['cost']
        season=request.POST['season']
        stock=request.POST['stock']
        pmodel=request.POST['pmodel']
        product.objects.create(pname=pname,img=url,cost=cost,season=season,pmodel=pmodel,stockavailable=stock)
        return render(request,'shop/update.html',{'msg':'update success'})
    else:
        return HttpResponse('cant update now')
          

        
        



             

# Create your views here.