from django.shortcuts import render, redirect
from .models import Member
from django.http import JsonResponse, HttpResponse
from .forms import SigupForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def index(request):
    all_members = Member.objects.all()
    return render(request, 'datatables/index.html', {'all_members': all_members})


def insert(request):
    member = Member(firstname=request.POST['firstname'], lastname=request.POST['lastname'],
                    address=request.POST['address'])
    member.save()
    return redirect('/')


@login_required
def show(request,id):
    try:
        m = Member.objects.filter(id=id)
        if m.exists():
            member = m.first()
        else:
            return HttpResponse('Data not found')
        return render(request,'datatables/show.html',{'member':member})
    except ValueError:
        return HttpResponse('String not allowed')



def update(request):
    if request.method == "POST":
        update_mem = Member.objects.get(id=request.POST.get('id'))
        update_mem.firstname = request.POST.get('firstname')
        update_mem.lastname = request.POST.get('lastname')
        update_mem.address = request.POST.get('address')
        update_mem.save()
        return JsonResponse({'sucess':200})


def userSignup(request):
    if request.method == "POST":
        userform = SigupForm(request.POST)
        if userform.is_valid():
            userform.save()
            messages.success(request,'Account Created Successfully')
    else:
        userform = SigupForm()
    return render(request,'signup.html',{'userform':userform})


def userLogin(request):
    uservalue=''
    passwordvalue=''
    valuenext= request.POST.get('next')
    if request.method == "POST":
        valuenext= request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None and valuenext=='':
            login(request,user)
            return redirect('/')
        if user is not None and valuenext !='':
            login(request, user)
            return redirect(valuenext)
        else:
            messages.error(request,'username or password is invalid')
    return render(request,'login.html')


def userLogout(request):
    logout(request)
    return redirect('/login/')
