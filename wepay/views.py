from django.shortcuts import get_object_or_404, render, redirect
#from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Payment, Payment_For_User
from . import models
from django.urls import reverse
from .utils import get_plot


def index(request):
    context = {}
    context["users"] = User.objects.all()
    context["payments"] = Payment.objects.all().order_by('-id')[:10]
    context["overall_payment_amount"] = models.get_overall_payment_amount()
    context["who_is_next"] = models.who_is_next()
    return render(request, "wepay/index.html", context)


def add_user(request):
    if "user_name" in request.POST:
        user = User()
        user.name = request.POST["user_name"]
        if user.name != None and user.name != "":
            user.save()
    return redirect('wepay:index')


def view_payment_form(request):
    context = {}
    context["users"] = User.objects.all()
    return render(request, "wepay/payment_form.html", context)


def add_payment(request):
    user_id = []
    for user in request.POST.getlist("user"):
        user_id.append(user)

    users = []
    for id in user_id:
        user = User.objects.get(pk=id)
        users.append(user)

    payment = Payment()
    payment.from_user = get_object_or_404(User,pk=request.POST["from_user_id"])
    payment.amount = request.POST["amount"]
    payment.description = request.POST["description"]
    payment.save()

    for user in users:
        payment_for_user = Payment_For_User()
        payment_for_user.user = user
        payment_for_user.payment = payment
        payment_for_user.save()

    return redirect('wepay:index')


def detail_user(request, user_id):
    context = {}
    context["user"] = get_object_or_404(User, pk=user_id)
    context["payments"] = Payment.objects.filter(from_user=user_id)
    
    if len(context["payments"]) > 0 or len(context["user"].payment_for_user_set.all()) > 0:
        context['deletable'] = False
    else:       
        context['deletable'] = True
        
    return render(request, 'wepay/detail_user.html', context)


def matplot_view(request):
    context = {}
    qs = User.objects.all()
    x = [x.name for x in qs]
    print (x)
    #y = []   
    #for user in qs:
        #i= user.get_saldo()
        #y.append(i)
    y = [y.get_saldo() for y in qs]
    print (y)
    context["chart"] = get_plot(x, y)
    return render(request, 'wepay/matplot.html', context)


def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)   
    if len(user.payment_set.all()) == 0 and len(user.payment_for_user_set.all()) == 0: 
        user.delete()
    return redirect('wepay:index')


def detail_payment(request, payment_id):
    context = {}
    context["payment"] = get_object_or_404(Payment, pk=payment_id)
    context["for_users"] = Payment_For_User.objects.filter(payment=payment_id)
    #test = Payment_For_User.objects.filter(payment=payment_id)
    #print("for_users:", test)
    return render(request, "wepay/detail_payment.html", context)


def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)    
    payment.delete()
    return redirect('wepay:index')


def edit_payment(request, payment_id):
    pass









