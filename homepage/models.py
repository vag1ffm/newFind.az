from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


def content_file_name(instance, filename):
    return '/'.join(['content', str(instance.created_by.id), filename])


class Tovar(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название Товара")
    title_small = models.CharField(max_length=255, null=True, verbose_name="Название товара для поиска")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    for_adult = models.BooleanField(default=False, verbose_name="Товар для взрослых")
    barcode = models.CharField(max_length=255, verbose_name="Штрих код")
    brand = models.CharField(max_length=255, verbose_name="Бренд или производитель")
    weight = models.CharField(max_length=20, verbose_name="Вес")
    height = models.CharField(max_length=20, verbose_name="Высота")
    width = models.CharField(max_length=20, verbose_name="Ширина")
    length = models.CharField(max_length=20, verbose_name="Длина")
    country_of_origin = models.CharField(max_length=255, verbose_name="Страна производства")
    producer = models.CharField(max_length=255, verbose_name="Изготовитель")
    age_to_use = models.CharField(max_length=255, verbose_name="С какого возраста пользоваться")
    expiration_date_for_meal = models.CharField(max_length=255, verbose_name="Срок годности")
    expiration_date_for_gadgets = models.CharField(max_length=255, verbose_name="Срок службы")
    guarantee_period = models.CharField(max_length=255, verbose_name="Гарантийный период")
    content = models.TextField(verbose_name="Описание Товара")
    content_small = models.TextField(null=True, verbose_name="Описание Товара")

    # photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    photo_main = models.ImageField(upload_to=content_file_name, verbose_name="Фото главное")
    photo_1 = models.ImageField(upload_to=content_file_name, verbose_name="Фото 1", blank=True)
    photo_2 = models.ImageField(upload_to=content_file_name, verbose_name="Фото 2", blank=True)
    photo_3 = models.ImageField(upload_to=content_file_name, verbose_name="Фото 3", blank=True)
    photo_4 = models.ImageField(upload_to=content_file_name, verbose_name="Фото 4", blank=True)
    photo_5 = models.ImageField(upload_to=content_file_name, verbose_name="Фото 5", blank=True)
    photo_6 = models.ImageField(upload_to=content_file_name, verbose_name="Фото 6", blank=True)
    photo_7 = models.ImageField(upload_to=content_file_name, verbose_name="Фото 7", blank=True)
    photo_8 = models.ImageField(upload_to=content_file_name, verbose_name="Фото 8", blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    price_with_skidka = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена со скидкой")

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время загрузки")

    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    podcat = models.ForeignKey('PodCat', on_delete=models.PROTECT, verbose_name="Подкатегории")
    podpodcat = models.ForeignKey('PodPodCat', on_delete=models.PROTECT, verbose_name="Подподкатегория")
    properties = models.JSONField(verbose_name="Характеристики в подподкатегории")

    created_by = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Кем добавлено")
    open_times = models.SmallIntegerField(default=0, verbose_name="Сколько раз открыто")

    rating = models.FloatField(default=0)

    rating_from_user = models.ManyToManyField("User", related_name="rating_user", through="Rating_andComments")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('showtovar', kwargs={"tovarslug": self.slug})

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-time_create']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True, verbose_name="Категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    icon = models.CharField(max_length=255, verbose_name="Класс иконки")
    topic = models.CharField(max_length=255, verbose_name="Класс категории")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={"catslug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['id']


class PodCat(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True, verbose_name="Подкатегория категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    maincat = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Основная категория")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('podcategory', kwargs={"podcatslug": self.slug})

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "ПодКатегории"
        ordering = ['id']


class PodPodCat(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True, verbose_name="Подподкатегория категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    maincat = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Основная категория")
    mainpodcat = models.ForeignKey("PodCat", on_delete=models.PROTECT, verbose_name="Подкатегория основной категории")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('podpodcategory', kwargs={"podpodcatslug": self.slug})

    class Meta:
        verbose_name = "ПодПодкатегория"
        verbose_name_plural = "ПодПодКатегории"
        ordering = ['id']


class User(AbstractUser):
    DEFAULT = 'Не указан'
    MALE = 'Мужчина'
    FEMALE = 'Женщина'
    OTHER = 'Другое'
    GENDER_CHOICES = [
        (DEFAULT, 'Не указан'),
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
        (OTHER, 'Другое'),
    ]
    username = models.CharField(max_length=25, unique=False)
    email = models.EmailField(_("email address"), unique=True)
    email_verify = models.BooleanField(default=False, verbose_name="Подтверждение аккаунта")
    conditions = models.BooleanField(default=False, verbose_name="Условия конфиденциальности")

    is_seller = models.BooleanField(default=False, verbose_name="Продавец или покупатель")

    birth_day = models.DateField(null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$',
        message="Номер телефона должен быть в формате: '+994 XX XXX XX XX'."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Номер телефона")
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=DEFAULT, verbose_name="Пол")
    occupation = models.CharField(max_length=50, verbose_name="Занятие", blank=True)
    address_type = models.CharField(max_length=255, verbose_name="Тип адреса", blank=True)
    city = models.CharField(max_length=50, verbose_name="Город", blank=True)
    place = models.CharField(max_length=255, verbose_name="Место", blank=True)
    place_slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name="URL")
    block_number = models.CharField(max_length=50, verbose_name="Номер блока", blank=True)

    store_rating = models.FloatField(default=0)

    user_favorite = models.ManyToManyField("Tovar", related_name='favorite_tovari')
    user_cart = models.ManyToManyField("Tovar", related_name="cart_tovari", through='MyCart')
    user_rating_and_comment_for_tovar = models.ManyToManyField("Tovar", related_name="rating_tovar", through="Rating_andComments")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_absolute_url(self):
        return reverse('profile', kwargs={"place_slug": self.place_slug})


class MyCart(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Пользователь")
    count = models.SmallIntegerField(default=1, verbose_name="Кол-во продукта")
    product = models.ForeignKey("Tovar", on_delete=models.CASCADE, verbose_name="Товар")


class Rating_andComments(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey("Tovar", on_delete=models.CASCADE, verbose_name="Товар")
    rating = models.FloatField(default=0, verbose_name="Рейтинг")
    plus = models.CharField(max_length=255, null=True, verbose_name="Плюсы товара")
    minus = models.CharField(max_length=255, null=True, verbose_name="Минусы товара")
    comment = models.TextField(null=True, verbose_name="Комментарий")
    time_cr = models.DateTimeField(null=True, auto_now_add=True, verbose_name="Время создания")
