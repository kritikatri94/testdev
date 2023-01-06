from django.shortcuts import render, redirect
from .models import Member
from django.http import JsonResponse


def index(request):
    all_members = Member.objects.all()
    return render(request, 'datatables/index.html', {'all_members': all_members})


def insert(request):
    member = Member(firstname=request.POST['firstname'], lastname=request.POST['lastname'],
                    address=request.POST['address'])
    member.save()
    return redirect('/')


def show(request,id):
    if request.method == "POST":
        update_mem = Member.objects.get(id=request.POST.get('id'))
        update_mem.firstname = request.POST.get('firstname')
        update_mem.lastname = request.POST.get('lastname')
        update_mem.address = request.POST.get('address')
        update_mem.save()
        return JsonResponse({'sucess':200})
    member = Member.objects.get(id=id)
    return render(request,'datatables/show.html',{'member':member})
