from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Buyer(models.Model):
    person = models.ForeignKey(User, on_delete=models.PROTECT)
    FIO = models.CharField(max_length=100, verbose_name='ФИО', default='')


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории', default='')


class Fiz_lico(models.Model):
    FIO = models.CharField(max_length=100, verbose_name='ФИО', default='')
    num_svidet = models.CharField(max_length=20, verbose_name='Номер свидетельства')


class Yur_lico(models.Model):
    name_of_company = models.CharField(max_length=100, verbose_name='Нахззвание компании', default='')
    nalog_num = models.CharField(max_length=20, verbose_name='Номер налоговый', default='')
    num_nds = models.CharField(max_length=20, verbose_name='Номер НДС', default='')


class Suppliers(models.Model):
    yur_lico = models.ForeignKey(Yur_lico, on_delete=models.PROTECT, null=True)
    fiz_lico = models.ForeignKey(Fiz_lico, on_delete=models.PROTECT, null=True)
    address = models.CharField(max_length=150, verbose_name='Адрес', default='')
    others = models.TextField(verbose_name='Остальная информация', default='')


class Tovar(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', default='')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    count = models.IntegerField(verbose_name='Количество товаров на складе')
    srok_godosti = models.IntegerField(verbose_name='Гарантийний срок(в днях)')
    price = models.IntegerField(verbose_name='цена')
    suppilers = models.ManyToManyField(Suppliers)


class Incoming(models.Model):
    product_id = models.ForeignKey(Tovar, on_delete=models.PROTECT)
    date = models.DateTimeField(verbose_name='Дата поставки')
    count = models.IntegerField(verbose_name='Количество')
    #   переопределить метод save() для увеличения кол-во единиц товара в строке таблицы Tovar


class Outgoing(models.Model):
    product_id = models.ForeignKey(Tovar, on_delete=models.PROTECT)
    date = models.DateTimeField(verbose_name='Дата отправки')
    count = models.IntegerField(verbose_name='Количество')
    #   переопределить метод save() для уменьшения кол-во единиц товара в строке таблицы Tovar


class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    tovar = models.ForeignKey(Tovar, on_delete=models.PROTECT)
    count = models.IntegerField(verbose_name='Количество')
    total_price = models.IntegerField(verbose_name='Сумма заказа', null=True)
