# Generated by Django 5.0.4 on 2024-04-24 13:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='Название категории')),
            ],
        ),
        migrations.CreateModel(
            name='Fiz_lico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FIO', models.CharField(default='', max_length=100, verbose_name='ФИО')),
                ('num_svidet', models.CharField(max_length=20, verbose_name='Номер свидетельства')),
            ],
        ),
        migrations.CreateModel(
            name='Yur_lico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_company', models.CharField(default='', max_length=100, verbose_name='Нахззвание компании')),
                ('nalog_num', models.CharField(default='', max_length=20, verbose_name='Номер налоговый')),
                ('num_nds', models.CharField(default='', max_length=20, verbose_name='Номер НДС')),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FIO', models.CharField(default='', max_length=100, verbose_name='ФИО')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='', max_length=150, verbose_name='Адрес')),
                ('others', models.TextField(default='', verbose_name='Остальная информация')),
                ('fiz_lico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='logic.fiz_lico')),
                ('yur_lico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='logic.yur_lico')),
            ],
        ),
        migrations.CreateModel(
            name='Tovar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='Название')),
                ('count', models.IntegerField(verbose_name='Количество товаров на складе')),
                ('srok_godosti', models.IntegerField(verbose_name='Гарантийний срок(в днях)')),
                ('price', models.IntegerField(verbose_name='цена')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='logic.category')),
                ('suppilers', models.ManyToManyField(to='logic.suppliers')),
            ],
        ),
        migrations.CreateModel(
            name='Outgoing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата отправки')),
                ('count', models.IntegerField(verbose_name='Количество')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='logic.tovar')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Количество')),
                ('total_price', models.IntegerField(null=True, verbose_name='Сумма заказа')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='logic.buyer')),
                ('tovar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='logic.tovar')),
            ],
        ),
        migrations.CreateModel(
            name='Incoming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата поставки')),
                ('count', models.IntegerField(verbose_name='Количество')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='logic.tovar')),
            ],
        ),
    ]
