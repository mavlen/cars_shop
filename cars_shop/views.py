from django.shortcuts import render, redirect
from django.http import HttpResponse

from cars_shop.models import Cars, Comment
from .forms import CommentForm

def slovo(request):
    return HttpResponse('Hello world')

def hello(request):
    cars = Cars.objects.all()
    # carsimages = .objects.all()
    return render(request, 'index.html',context = {"cars":cars})

def cars(request):
    return HttpResponse('Hello world')
    
def cars(request):
    cars = Cars.objects.all()
    # carsimages = .objects.all()
    return render(request, 'cars.html',context = {"cars":cars})


# def get_list(request):
#     reg = Name.objects.all()
#     return render(request, 'spisok.html', {'reg':reg})

# def cars_shop_detail(request, pk):
#     details = Name.objects.filter(pk=pk)
#     return render(request, 'details.html', {'details':details})


def car_detail(request, pk):
    car = Cars.objects.get(pk=pk)
    return render(request, 'car_detail.html', context = {'car':car})

def book_now(request, pk):
    car = Cars.objects.get(pk=pk)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        Comment.objects.create(
            name=form.data['name'], 
            email = form.data['email'], 
            number = form.data['number'],
            )
        return render(request, 'book_now.html', context = {'car':car,'form':form })
    return render(request, 'book_now.html', context = {'car':car,'form':form })
