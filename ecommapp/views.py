from django.shortcuts import render,redirect
from django.http import HttpResponse
from ecommapp.models import Product,Cart,Order
from django.db.models import Q
from ecommapp.forms import EmpForm,ProductModelForm,UserForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import random
import razorpay
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.

def home(request):
    #data=Product.objects.all()  #feth product active deactive
    #print(data)
    data=Product.objects.filter(status=1)#fetch only active rec
    content={}
    content['products']=data
    return render(request,'index.html',content)

'''def index(request): #for index atrribute error
    #data=Product.objects.all()  #feth product active deactive
    #print(data)
    data=Product.objects.filter(status=1)#fetch only active rec
    content={}
    content['products']=data
    return render(request,'index.html',content)
'''
'''
def login(request):
    return render(request,'login.html')
'''


def signup(request):
    return render(request,'signup.html')

#def haveac(request):
   # return render(request,'login.html')



def delete(request,rid):
    print("Id to be deleted:",rid)
    return HttpResponse("Id to be deleted:"+rid)

def edit(request,rid):
    print("Id to be edited:",rid)
    return HttpResponse("Id to be edited:"+rid)

def addition(request,x,y):
    z=int(x)+int(y)
    print("Addition is:",z)
    return HttpResponse("Addition is:"+str(z))

def user_register(request):
    return render(request,'register.html')


def product_list(request):

    context={}
    context['name']="Samsung"
    context['x']=1000
    context['y']=200
    context['data']=[10,20,30,40,50]
    context['plist']=[
        {'name':'Samsung','pimage':'image of samsung','price':30000,'desc':'Product description'},
        {'name':'iphone','pimage':'image of iphone','price':85000,'desc':'Product description'},
        {'name':'Vivo','pimage':'image of vivo','price':35000,'desc':'Product description'},
    ]
    return render(request,'productlist.html',context)

def reuse(request):
    return render (request,'base.html')

#sorting function
def sort(request,sv):
    if sv=='0':
        param='price'
    else:
        param='-price'

    data=Product.objects.order_by(param).filter(status=1)
    content={}
    content['products']=data
    return render(request,'index.html',content)

def catfilter(request,catv):
    q1=Q(cat=catv)
    q2=Q(status=1)
    data=Product.objects.filter(q1 & q2)
    content={}
    content['products']=data
    return render(request,'index.html',content)

def pricefilter(request,pv):
    q1=Q(status=1)
    if pv=='0':
        q2=Q(price__lt=5000)
    else:
        q2=Q(price__gte=5000)

    data=Product.objects.filter(q1 & q2)
    content={}
    content['products']=data
    return render(request,'index.html',content)

def pricerange(request):
    low=request.GET['min']
    high=request.GET['max']
    #print(low)
    #print(high)
    q1=Q(status=1)
    q2=Q(price__gte=low)
    q3=Q(price__lte=high)

    data=Product.objects.filter(q1 & q2 & q3)
    content={}
    content['products']=data
    return render(request,'index.html',content)

   
   #For Product details

def product_details(request,pid):
    #print("Id of the product:",pid)
    data=Product.objects.filter(id=pid)
    content={}
    content['products']=data
    return render(request,'product_details.html',content)

def addproduct(request):
    
    #print("Method is:",request.method)
    if request.method=="POST":
        #print("insert record into the database")
        #insert data into data base the table product
        #fetch data from request post
     n=request.POST['pname']
     c=request.POST['pcat']
     amt=request.POST['pprice']
     s=request.POST['status']
        #print(n)
        #print(cat)
        #print(amt)
        #print(s)
     p=Product.objects.create(name=n,cat=c,price=amt,status=s)
        #print(p)
     p.save()
     return redirect('/addproduct')

    else:
     #print("in else part")
     p=Product.objects.all()
     content={}
     content['products']=p
     return render(request,'addproduct.html',content)
    
def delproduct(request,rid):
     #print("ID to be deleted:",rid)
     #fetch record to be deletd
     p=Product.objects.filter(id=rid)
     p.delete()
     return redirect('/addproduct')

def editproduct(request,rid):
    p=Product.objects.filter(id=rid)
    p.edit()
    return redirect('/addproduct')

def djangoform(request):
    if request.method =='POST':
        ename=request.POST['name']
        dept=request.POST['dept']
        email=request.POST['email']
        salary=request.POST['salary']
        print(ename)
        print(dept)
        print(email)
        print(salary)
    else:
        eobj=EmpForm()
        content={}
        content['forms']=eobj
        return render(request,'djangoform.html',content)


def modelform(request):
    if request.method=='POST':
        name=request.POST['name']
        cat=request.POST['cat']
        price=request.POST['price']
        status=request.POST['status']
        pimage=request.POST['pimage']
        print('Product Name:',name)
        print('Product Category:',cat)
        print('Product Price:',price)
        print('Product status:',status)
        print('Image Path:',pimage)
    else:
        pobj=ProductModelForm()
        content={}
        content['forms']=pobj
        return render(request,'modelform.html',content)
    


def user_register(request):
    content={}
    regobj=UserForm()
    content['userform']=regobj

    if request.method=='POST':
        regobj=UserForm(request.POST)
        #print(regobj)
        #print(regobj.is_valid())
        if regobj.is_valid():
            regobj.save()
            content['success']="User Created Successfully"
            return render(request,'user_register.html',content)
        
    else:
        #regobj=UserCreationForm()
        #print(regobj)
        
        return render(request,'user_register.html',content)
    
def user_login(request):
    if request.method=="POST":
        dataobj=AuthenticationForm(request=request,data=request.POST)
        print(dataobj)

        if dataobj.is_valid():
            uname=dataobj.cleaned_data['username']
            upass=dataobj.cleaned_data['password']
            #print("username:",uname)
            #print("password:",upass)
            u=authenticate(username=uname,password=upass)
            #print(u)
            if u:
                login(request,u)
                return redirect("/")
            
            else:
                eobj=AuthenticationForm()
                content={} 
                content['loginform']=eobj
                return render(request,'user_login.html',content)
            


    else:
        obj=AuthenticationForm()
        content={}
        content['loginform']=obj
        return render(request,'user_login.html',content)


def setsession(request):

    request.session['name']='Rohit'
    return render(request,'setsession.html')

def getsession(request):
    content={}
    content['data']=request.session['name']
    return render(request,'getsession.html',content)
    
def addtocart(request,pid):

    if request.user.is_authenticated:
        userid=request.user.id
        #check wether user already added product in cart
        q1=Q(pid=pid)
        q2=Q(uid=userid)
        c=Cart.objects.filter(q1 & q2)
        p=Product.objects.filter(id=pid)
        content={}
        content['products']=p
        if c:
            content['msg']="Product Already Exist in the cart"
            return render(request,'product_details.html',content)
        else:
            #print(" User ID:",uid)
            #print(" Product ID:",pid)
            u=User.objects.filter(id=userid)
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            content['success']="Product Added in Cart"
            return render(request,'product_details.html',content)

    else:
        return redirect('/login')

def user_logout(request):
    
    logout(request)
    return redirect('/login')


def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    sum=0
    for x in c:
        sum=sum+(x.qty*x.pid.price)
        print("Total Product Price:",sum)
    content={}
    content['products']=c
    content['nitems']=len(c)
    content['total']=sum
    return render(request,'viewcart.html',content)


def changeqty(request,pid,f):
    content={}
    c=Cart.objects.filter(pid=pid)
    if f=='1':
        x=c[0].qty+1  #c.qty+1
    else:
        x=c[0].qty-1

    if x>0:
        c.update(qty=x)
    return redirect('/viewcart')


def placeorder(request):
    oid=random.randrange(1000,9999)
    #print(oid)
    user_id=request.user.id
    c=Cart.objects.filter(uid=user_id)
    #print(c)
    for x in c:
       o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
       o.save()
       x.delete()

    o=Order.objects.filter(uid=user_id)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)
    content={}
    content['products']=o
    content['nitems']=len(o)
    content['total']=sum

    return render(request,'placeorder.html',content)

def makepayment(request):
    user_id=request.user.id
    client = razorpay.Client(auth=("rzp_test_KLuc8q5Pngg5XZ", "ftAymVb196pQvWtafzWAM5GE"))
    o=Order.objects.filter(uid=user_id)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)
    sum=sum*100  #for conversion into paisa
    data = { "amount":sum, "currency": "INR", "receipt":str(o[0].id)}
    #oid=str(o[0].id)
    payment = client.order.create(data=data)
    print(payment)
    content={}
    content['payment']=payment
    return render(request,'pay.html',content)

def storedetails(request):
    pay_id=request.GET['pid']
    order_id=request.GET['oid']
    sign=request.GET['sign']
    userid=request.user.id
    u=User.objects.filter(id=userid)

    #print(pay_id)
    #print(order_id)
    #print(sign)
    email=u[0].email
    msg="Your Order Is Placed Successfully. Details are Payment ID:"+pay_id+" and Order ID is:"+order_id+""
    send_mail(
    "Order Status-Ecart",
    msg,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
    )

    return HttpResponse("Payment success")