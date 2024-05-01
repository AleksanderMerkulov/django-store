from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from logic.forms import changeInfoForm, buyTovar
from logic.models import Tovar, Buyer


# Create your views here.
def mainPage(request):
    products = Tovar.objects.all()
    return render(request, 'pages/main_page.html', {
        'products': products
    })
    pass


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    redirect_field_name = "home"


class LogoutUser(LogoutView):
    template_name = 'registration/login.html'


def change_profile(request):
    p = Buyer.objects.filter(person_id=request.user.id)

    if not p:
        if request.method == "GET":
            form = changeInfoForm()
            return render(request, 'forms/form.html', {'form': form})

        if request.method == "POST":
            form = changeInfoForm(request.POST)
            n_form = form.save(commit=False)
            exists = Buyer.objects.filter(passport=n_form.passport).exists()
            if exists:
                return render(request, 'forms/form.html', {'form': form, 'err': 'Такие паспортные данные существуют'})
            n_form.person_id = request.user.id
            n_form.save()
            return redirect('/')
    else:
        person = Buyer.objects.get(person_id=request.user.id)
        if request.method == "GET":
            form = changeInfoForm(instance=person)
            return render(request, 'forms/form.html', {'form': form})

        if request.method == "POST":
            form = changeInfoForm(request.POST, instance=person)
            return redirect('/')


def show_logs(request):
    if request.user.is_superuser:
        logs = LogEntry.objects.all()
        return render(request, "pages/logs.html", {'logs': logs})
    else:
        return render(request, 'pages/not_allowed.html')


def show_curr_tovar(request, pk):
    tovar = get_object_or_404(Tovar, id=pk)
    return render(request, 'pages/curr_tovar.html', {'tovar': tovar})


@login_required
def buy_curr_tovar(request, pk):
    tovar = get_object_or_404(Tovar, id=pk)
    if request.method == "GET":
        form = buyTovar()
        return render(request, 'forms/form.html', {'form': form,
                                                   'tovar': tovar})
    if request.method == "POST":
        form = buyTovar(request.POST)
        n_form = form.save(commit=False)
        n_form.buyer_id = request.user.id
        n_form.tovar_id = int(pk)
        n_form.total_price = n_form.count * tovar.price
        n_form.save()
        return redirect(f'/product/{pk}')
