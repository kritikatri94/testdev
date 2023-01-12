from django.shortcuts import render, redirect
from .models import Member
from django.http import JsonResponse, HttpResponse
from .forms import SigupForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views import View
from myapp.helpers import check_unique_name


'''def index(request):
    all_members = Member.objects.all()
    return render(request, 'datatables/index.html', {'all_members': all_members})'''

class IndexView(View):
    def get(self,request):
        all_member = Member.objects.all()
        return render(request,'datatables/index.html',{'all_members':all_member})
    
    def post(self,request):
        all_member = Member.objects.all()
        if 'delete' in request.POST:
            Member.objects.get(id=request.POST.get('id')).delete()
            messages.success(request,'Member Deleted !!')
            return render(request,'datatables/index.html',{'all_members':all_member})


'''def insert(request):
    member = Member(firstname=request.POST['firstname'], lastname=request.POST['lastname'],
                    address=request.POST['address'])
    member.save()
    return redirect('/')'''

class InsertView(View):
    def post(self,request):
        member = Member(firstname=request.POST['firstname'], lastname=request.POST['lastname'],
                    address=request.POST['address'])
        member.save()
        return redirect('index')


'''@login_required
def show(request,id):
    try:
        m = Member.objects.filter(id=id)
        if m.exists():
            member = m.first()
        else:
            return HttpResponse('Data not found')
        return render(request,'datatables/show.html',{'member':member})
    except ValueError:
        return HttpResponse('String not allowed')'''


class ShowView(View):
    def get(self,request,pk):
        try:
            m = Member.objects.filter(id=pk)
            if m.exists():
                member = m.first()
            else:
                return HttpResponse('Data not found')
            return render(request,'datatables/show.html',{'member':member})
        except ValueError:
            return HttpResponse('String not allowed')


'''def update(request):
    if request.method == "POST":
        update_mem = Member.objects.get(id=request.POST.get('id'))
        update_mem.firstname = request.POST.get('firstname')
        update_mem.lastname = request.POST.get('lastname')
        update_mem.address = request.POST.get('address')
        update_mem.save()
        return JsonResponse({'sucess':200})'''


class UpdateView(View):
    def post(self,request):
        update_mem = Member.objects.get(id=request.POST.get('id'))
        update_mem.firstname = request.POST.get('firstname')
        update_mem.lastname = request.POST.get('lastname')
        update_mem.address = request.POST.get('address')
        update_mem.save()
        return JsonResponse({'sucess':200})


'''def userSignup(request):
    if request.method == "POST":
        userform = SigupForm(request.POST)
        if userform.is_valid():
            userform.save()
            messages.success(request,'Account Created Successfully')
    else:
        userform = SigupForm()
    return render(request,'signup.html',{'userform':userform})'''

class UsersignupView(View):
    def get(self,request):
        userform = SigupForm()
        return render(request,'signup.html',{'userform':userform})

    def post(self,request):
        userform = SigupForm(request.POST)
        if userform.is_valid():
            userform.save()
            messages.success(request,'Account Created Successfully')
        return render(request,'signup.html',{'userform':userform})


'''def userLogin(request):
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
    return render(request,'login.html')'''

class UserloginView(View):
    def post(self,request):
        valuenext= request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if not username and not password:
            return render(request,'login.html',{'username_password_required':True,'username':username})
        if not username:
            return render(request,'login.html',{'username_required':True,'username':username})
        if not password:
            return render(request,'login.html',{'password_required':True,'username':username})
        if user is not None and valuenext=='':
            login(request,user)
            return redirect('index')
        if user is not None and valuenext !='':
            login(request, user)
            return redirect(valuenext)
        else:
            messages.error(request,'Username or Password is invalid')
        return render(request,'login.html')
    
    def get(self,request):
        return render(request,'login.html')


'''def userLogout(request):
    logout(request)
    return redirect('/login/')'''


class UserlogoutView(View):
    def post(self,request):
        logout(request)
        return redirect('userLogin')


class UpdatememberView(View):
    def post(self,request):
        id = request.POST.get('id')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        if check_unique_name(id, firstname, lastname):
            member = Member.objects.get(id=id)
            member.firstname = firstname
            member.lastname = lastname
            member.save()
            return JsonResponse({'status':200})
        return JsonResponse({'status':401})