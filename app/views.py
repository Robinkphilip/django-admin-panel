from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
# Create your views here.


#.....................................admin section....................................

#@never_cache
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# def adminhome(request):
#         return render(request,'adminlogin.html')

#@never_cache
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/adminlogin')
def adminpanel(request):
    if request.user.is_superuser:
        data = User.objects.all().exclude(is_superuser=True).order_by('id')
        context = {'data': data}  
        return render(request, 'adminpanel.html', context)
    else:
        return redirect('/')
        

def insert(request):
    data=User.objects.all().exclude(is_superuser=True).order_by('id')
    context={'data':data}
    if request.method=="POST":
        name=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('pass1')
        password2=request.POST.get('pass2')

        if password1 != password2:
            messages.warning(request,'Password is incorrect')
            return redirect('/insert')

        if User.objects.filter(username=name):
            messages.warning(request,'username already taken')
            return redirect('/insert')
        
        if User.objects.filter(email=email):
            messages.warning(request,'Email is already taken')
            return redirect('/insert')
        
        myadmin=User.objects.create_user(name,email,password1)
        myadmin.save()
         
        messages.success(request,'Added Sucessfully')

    return render(request,'adminpanel.html',context) 

#@never_cache
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def update(request,id):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        edit=User.objects.get(id=id)
        edit.username=username
        edit.email=email
        edit.save()
        return redirect("/adminpanel")
    
    d=User.objects.get(id=id)
    context={"d":d}
    return render(request,"edit.html",context)

#@never_cache
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def delete(request,id):
    d=User.objects.get(id=id) 
    d.delete()
    return redirect('/adminpanel')


def search(request):
    username = request.GET.get('searchname')
    if username is not None:
        data = User.objects.filter(username__icontains=username).exclude(is_superuser=True).order_by('id')
        context={"data":data}
        return render(request,"adminpanel.html",context)

    return redirect("/adminpanel")
   

#@never_cache
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
# @cache_control(no_cache=True, no_store=True)
def adminlogin(request):
    if request.user.is_authenticated:
        return redirect('/adminpanel')
    
    if request.method=="POST":
        fullname=request.POST.get('username')
        password=request.POST.get('pass1')
       
        myadmin=authenticate(username=fullname,password=password)
       
        if myadmin is not None and myadmin.is_superuser:
            login(request,myadmin)

            messages.success(request,'login sucess')
            return redirect('/adminpanel')
        else:
            messages.warning(request,'Invalid credentials')

    return render(request,'adminlogin.html')

#@never_cache
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/adminlogin')
def logoutAdmin(request):
    logout(request)
    return redirect('/adminlogin')




###############################################...LOGIN PAGE...##################################################




@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/login')
def home(request):
    if request.user.is_superuser:
        logout(request)
        return redirect('/login') 
    else:
        return render(request,'index.html')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def handlesignup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        uname=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        conformpass=request.POST.get("conformpass")

        if password!=conformpass:
            messages.warning(request,"Password is Incorrect")
            return redirect('/signup')
        
        try:
            if User.objects.get(username=uname):
                 
                 messages.warning(request,"Username is already taken")
                 return redirect('/signup')
        except:
            pass

        try:
            if User.objects.get(email=email):
                 messages.warning(request,"Email is already taken")
                 return redirect('/signup')
        except:
            pass

        myuser=User.objects.create_user(uname,email,password)
        myuser.save()

        messages.success(request,"Signup Successful Please login!")
        return redirect('/login')
       

    return render(request,'signup.html')
    

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def handlelogin(request):

    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        uname=request.POST.get("username")
        password=request.POST.get("password1")
        myuser=authenticate(username=uname,password=password)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"login Success")
            return redirect('/')
        else: 
             messages.error(request,"Invalid Credentials")
             return redirect('/login')
    return render(request,'login.html')


@login_required(login_url='/')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/login')