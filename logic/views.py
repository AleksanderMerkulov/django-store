import io

from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle, Table, SimpleDocTemplate

from logic.forms import changeInfoForm, buyTovar
from logic.models import Tovar, Buyer, Order


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


def profile(request):
    userInfo = get_object_or_404(Buyer, person_id = request.user.id)
    orders = Order.objects.filter(buyer_id=request.user.id)
    return render(request, 'pages/profile.html', {
        'userInfo': userInfo,
        'orders': orders
    })


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
        if tovar.count <= 0 | tovar.count < n_form.count:
            return render(request, 'forms/form.html', {'form': form,
                                                       'tovar': tovar,
                                                       'err': "Недостаточно товаров на складе"})
        n_form.save()
        return redirect(f'/product/{pk}')


def otchet(request):
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    orders = Order.objects.all()

    # Настройка PDF
    pdf_filename = "all_orders.pdf"
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Определение стилей
    styles = getSampleStyleSheet()
    styleH = styles["Heading1"]

    # Форматирование данных в виде списка списков для таблицы
    table_data = [['Number', 'Buyer', 'Product', 'Count', 'Total price']]  # заголовки таблицы
    for entry in orders:
        tovar = f"{entry.tovar_id}|{entry.tovar.name}"
        table_data.append([entry.id, entry.buyer, tovar, entry.count, entry.total_price])  # добавление данных из модели

    # Создание таблицы с данными
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                               ]))

    # Добавление таблицы в элементы PDF
    elements.append(table)

    # Генерация PDF
    doc.build(elements)

    # Сброс указателя потока обратно в начало
    buffer.seek(0)

    # Создание FileResponse
    response = FileResponse(buffer, as_attachment=True, filename='all_orders.pdf')

    return response


def chek(request, pk):
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    order = Order.objects.get(id=pk)

    # Настройка PDF
    pdf_filename = "order.pdf"
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Определение стилей
    styles = getSampleStyleSheet()
    styleH = styles["Heading1"]

    # Форматирование данных в виде списка списков для таблицы
    table_data = [['Number', 'Buyer', 'Product', 'Count', 'Total price']]  # заголовки таблицы

    tovar = f"{order.tovar_id}|{order.tovar.name}"
    table_data.append([order.id, order.buyer, tovar, order.count, order.total_price])  # добавление данных из модели

    # Создание таблицы с данными
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                               ]))

    # Добавление таблицы в элементы PDF
    elements.append(table)

    # Генерация PDF
    doc.build(elements)

    # Сброс указателя потока обратно в начало
    buffer.seek(0)

    # Создание FileResponse
    response = FileResponse(buffer, as_attachment=True, filename='order.pdf')

    return response

