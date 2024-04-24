from django.contrib.auth.models import User
from django.db import models, router


# Create your models here.


class Buyer(models.Model):
    person = models.ForeignKey(User, on_delete=models.PROTECT)
    FIO = models.CharField(max_length=100, verbose_name='ФИО', default='')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return self.FIO


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории', default='')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Fiz_lico(models.Model):
    FIO = models.CharField(max_length=100, verbose_name='ФИО', default='')
    num_svidet = models.CharField(max_length=20, verbose_name='Номер свидетельства')

    class Meta:
        verbose_name = 'Физ.лицо'
        verbose_name_plural = 'Физ.лица'

    def __str__(self):
        return self.FIO


class Yur_lico(models.Model):
    name_of_company = models.CharField(max_length=100, verbose_name='Нахззвание компании', default='')
    nalog_num = models.CharField(max_length=20, verbose_name='Номер налоговый', default='')
    num_nds = models.CharField(max_length=20, verbose_name='Номер НДС', default='')

    class Meta:
        verbose_name = 'Юр.лицо'
        verbose_name_plural = 'Юр.лица'

    def __str__(self):
        return self.name_of_company


class Suppliers(models.Model):
    yur_lico = models.ForeignKey(Yur_lico, on_delete=models.PROTECT, null=True, blank=True)
    fiz_lico = models.ForeignKey(Fiz_lico, on_delete=models.PROTECT, null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name='Адрес', default='')
    others = models.TextField(verbose_name='Остальная информация', default='')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return "Поставщик {}{}".format(self.yur_lico.name_of_company, self.fiz_lico.FIO)


class Tovar(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', default='')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    count = models.IntegerField(verbose_name='Количество товаров на складе')
    srok_godosti = models.IntegerField(verbose_name='Гарантийний срок(в днях)')
    price = models.IntegerField(verbose_name='цена')
    suppilers = models.ManyToManyField(Suppliers)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return "Товар " + self.name + " | колво: " + str(self.count)


class Incoming(models.Model):
    product_id = models.ForeignKey(Tovar, on_delete=models.PROTECT)
    date = models.DateTimeField(verbose_name='Дата поставки')
    count = models.IntegerField(verbose_name='Количество')

    #   переопределить метод save() для увеличения кол-во единиц товара в строке таблицы Tovar
    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Save the current instance. Override this in a subclass if you want to
        control the saving process.

        The 'force_insert' and 'force_update' parameters can be used to insist
        that the "save" must be an SQL insert or update (or equivalent for
        non-SQL backends), respectively. Normally, they should not be set.
        """
        self._prepare_related_fields_for_save(operation_name="save")

        using = using or router.db_for_write(self.__class__, instance=self)
        if force_insert and (force_update or update_fields):
            raise ValueError("Cannot force both insert and updating in model saving.")

        deferred_non_generated_fields = {
            f.attname
            for f in self._meta.concrete_fields
            if f.attname not in self.__dict__ and f.generated is False
        }
        if update_fields is not None:
            # If update_fields is empty, skip the save. We do also check for
            # no-op saves later on for inheritance cases. This bailout is
            # still needed for skipping signal sending.
            if not update_fields:
                return

            update_fields = frozenset(update_fields)
            field_names = self._meta._non_pk_concrete_field_names
            non_model_fields = update_fields.difference(field_names)

            if non_model_fields:
                raise ValueError(
                    "The following fields do not exist in this model, are m2m "
                    "fields, or are non-concrete fields: %s"
                    % ", ".join(non_model_fields)
                )

        # If saving to the same database, and this model is deferred, then
        # automatically do an "update_fields" save on the loaded fields.
        elif (
                not force_insert
                and deferred_non_generated_fields
                and using == self._state.db
        ):
            field_names = set()
            for field in self._meta.concrete_fields:
                if not field.primary_key and not hasattr(field, "through"):
                    field_names.add(field.attname)
            loaded_fields = field_names.difference(deferred_non_generated_fields)
            if loaded_fields:
                update_fields = frozenset(loaded_fields)
        tovar = Tovar.objects.get(id=self.product_id)
        tovar.count = tovar.count + self.count
        tovar.save()
        self.save_base(
            using=using,
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )

    def __str__(self):
        return "Псотавка №" + str(self.id)


class Outgoing(models.Model):
    product_id = models.ForeignKey(Tovar, on_delete=models.PROTECT)
    date = models.DateTimeField(verbose_name='Дата отправки')
    count = models.IntegerField(verbose_name='Количество')

    #   переопределить метод save() для уменьшения кол-во единиц товара в строке таблицы Tovar
    class Meta:
        verbose_name = 'Отправка'
        verbose_name_plural = 'Отправки'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Save the current instance. Override this in a subclass if you want to
        control the saving process.

        The 'force_insert' and 'force_update' parameters can be used to insist
        that the "save" must be an SQL insert or update (or equivalent for
        non-SQL backends), respectively. Normally, they should not be set.
        """
        self._prepare_related_fields_for_save(operation_name="save")

        using = using or router.db_for_write(self.__class__, instance=self)
        if force_insert and (force_update or update_fields):
            raise ValueError("Cannot force both insert and updating in model saving.")

        deferred_non_generated_fields = {
            f.attname
            for f in self._meta.concrete_fields
            if f.attname not in self.__dict__ and f.generated is False
        }
        if update_fields is not None:
            # If update_fields is empty, skip the save. We do also check for
            # no-op saves later on for inheritance cases. This bailout is
            # still needed for skipping signal sending.
            if not update_fields:
                return

            update_fields = frozenset(update_fields)
            field_names = self._meta._non_pk_concrete_field_names
            non_model_fields = update_fields.difference(field_names)

            if non_model_fields:
                raise ValueError(
                    "The following fields do not exist in this model, are m2m "
                    "fields, or are non-concrete fields: %s"
                    % ", ".join(non_model_fields)
                )

        # If saving to the same database, and this model is deferred, then
        # automatically do an "update_fields" save on the loaded fields.
        elif (
                not force_insert
                and deferred_non_generated_fields
                and using == self._state.db
        ):
            field_names = set()
            for field in self._meta.concrete_fields:
                if not field.primary_key and not hasattr(field, "through"):
                    field_names.add(field.attname)
            loaded_fields = field_names.difference(deferred_non_generated_fields)
            if loaded_fields:
                update_fields = frozenset(loaded_fields)
        tovar = Tovar.objects.get(id=self.product_id)
        tovar.count = tovar.count - self.count
        tovar.save()
        self.save_base(
            using=using,
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )

    def __str__(self):
        return "Отправка №" + str(self.id)


class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    tovar = models.ForeignKey(Tovar, on_delete=models.PROTECT)
    count = models.IntegerField(verbose_name='Количество')
    total_price = models.IntegerField(verbose_name='Сумма заказа', null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Save the current instance. Override this in a subclass if you want to
        control the saving process.

        The 'force_insert' and 'force_update' parameters can be used to insist
        that the "save" must be an SQL insert or update (or equivalent for
        non-SQL backends), respectively. Normally, they should not be set.
        """
        self._prepare_related_fields_for_save(operation_name="save")

        using = using or router.db_for_write(self.__class__, instance=self)
        if force_insert and (force_update or update_fields):
            raise ValueError("Cannot force both insert and updating in model saving.")

        deferred_non_generated_fields = {
            f.attname
            for f in self._meta.concrete_fields
            if f.attname not in self.__dict__ and f.generated is False
        }
        if update_fields is not None:
            # If update_fields is empty, skip the save. We do also check for
            # no-op saves later on for inheritance cases. This bailout is
            # still needed for skipping signal sending.
            if not update_fields:
                return

            update_fields = frozenset(update_fields)
            field_names = self._meta._non_pk_concrete_field_names
            non_model_fields = update_fields.difference(field_names)

            if non_model_fields:
                raise ValueError(
                    "The following fields do not exist in this model, are m2m "
                    "fields, or are non-concrete fields: %s"
                    % ", ".join(non_model_fields)
                )

        # If saving to the same database, and this model is deferred, then
        # automatically do an "update_fields" save on the loaded fields.
        elif (
                not force_insert
                and deferred_non_generated_fields
                and using == self._state.db
        ):
            field_names = set()
            for field in self._meta.concrete_fields:
                if not field.primary_key and not hasattr(field, "through"):
                    field_names.add(field.attname)
            loaded_fields = field_names.difference(deferred_non_generated_fields)
            if loaded_fields:
                update_fields = frozenset(loaded_fields)
        tovar = Tovar.objects.get(id=self.tovar_id)
        tovar.count = tovar.count - self.count
        tovar.save()
        self.save_base(
            using=using,
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )

    def __str__(self):
        return "Заказ №" + str(self.id)
