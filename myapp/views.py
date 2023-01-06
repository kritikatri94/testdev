from django.shortcuts import render, redirect
from .models import Member


# Create your views here.
def index(request):
    all_members = Member.objects.all()
    return render(request, 'datatables/index.html', {'all_members': all_members})


def insert(request):
    member = Member(firstname=request.POST['firstname'], lastname=request.POST['lastname'],
                    address=request.POST['address'])
    member.save()
    return redirect('/')

