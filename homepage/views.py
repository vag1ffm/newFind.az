import random

from django.contrib import auth
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.core.checks import messages
from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
# from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage

from django.contrib.auth.decorators import login_required
from unidecode import unidecode
from django.template import defaultfilters

# from transliterate import slugify

from TestSite import settings
from .forms import *
from .models import *
from .utils import *

import json


az_to_en_for_slug = {
    'ə': 'e',
    'ğ': 'g',
    'ö': 'o',
    'ş': 'sh',
    'ç': 'c',
    'ı': 'i',
    'ü': 'u'
}


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# class MainHome(DataMixin, ListView):
#     model = Category
#     template_name = "homepage/index.html"
#     context_object_name = "categorii"
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="FindAz - Главная страница")
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def get_queryset(self):
#         c = Category.objects.all()
#         spisok = []
#         for i in c:
#             t = i.tovar_set.all()
#             spisok.append(t)
#
#         # return Tovar.objects.filter(is_published=True)
#         return spisok


def mainhome(request):
    podpodcats = PodPodCat.objects.all()
    spisok = [i.tovar_set.all()[:10] for i in podpodcats]
    #random.shuffle(spisok)

    paginator = Paginator(spisok, 3)

    if is_ajax(request=request):
        page = request.GET.get('page', None)

        try:
            tovari = paginator.page(int(page))
        except PageNotAnInteger:
            tovari = paginator.page(1)
        except InvalidPage:
            tovari = paginator.page(paginator.num_pages)
        temp = {}
        tovari_li = tovari.object_list
        for i in tovari_li:
            a = serializers.serialize('json', i)
            a = json.loads(a)
            temp[i[0].podpodcat.name] = a

        response = {
            'has_previous': tovari.has_previous(),
            'has_next': tovari.has_next(),
            'num_pages': tovari.paginator.num_pages,
            'tovari': temp
        }

        return JsonResponse(response)

    if request.method == 'GET':
        categorii = Category.objects.all()
        podcats = PodCat.objects.all()

        tovari = paginator.page(1)
        tovari_li = tovari.object_list
        random.shuffle(tovari_li)

        try:
            fav_user = auth.get_user(request)
            fav_tovari = fav_user.user_favorite.all()
            cart_tovari = fav_user.user_cart.all()
        except:
            fav_user = ""
            fav_tovari = []
            cart_tovari = []

        context = {
            'podcats': tovari_li,
            'categorii': categorii,
            'cats': categorii,
            'pcats': podcats,
            'ppcats': podpodcats,
            'fav_tovari': fav_tovari,
            'fav_tovari_id_list': [i.id for i in fav_tovari],
            'cart_tovari': cart_tovari,
            'cart_tovari_id_list': [i.id for i in cart_tovari],
            'salesman': fav_user,
            'title': 'FindAz - Главная страница'
        }
        return render(request, 'homepage/index.html', context=context)


def show_profile(request, place_slug):
    # salesman = auth.get_user(request)
    salesman = User.objects.get(place_slug=place_slug)
    tovari = Tovar.objects.filter(created_by=salesman.id)
    cats = Category.objects.all()
    podcats = PodCat.objects.all()
    ppodcats = PodPodCat.objects.all()
    podpodcats = list(set([i.podpodcat for i in tovari]))
    ppc_tovars = PodPodCat.objects.all()
    spisok = [i.tovar_set.filter(created_by=salesman.id) for i in ppc_tovars if i.tovar_set.filter(created_by=salesman.id)]

    try:
        fav_user = auth.get_user(request)
        fav_tovari = fav_user.user_favorite.all()
        cart_tovari = fav_user.user_cart.all()
    except:
        fav_user = ""
        fav_tovari = []
        cart_tovari = []

    data = {
        "salesman": salesman,
        "tovari": tovari,
        "cats": cats,
        "pcats": podcats,
        "ppcats": ppodcats,
        "podpodcats": podpodcats,
        "spisok": spisok,
        "title": salesman.occupation,
        'fav_tovari': fav_tovari,
        'cart_tovari': cart_tovari,
    }
    return render(request, "homepage/profile.html", data)


# class AddTovar(LoginRequiredMixin, DataMixin, CreateView):
#     form_class = AddTovarForm
#     template_name = 'homepage/adding-tovar.html'
#     login_url = reverse_lazy('home')
#     raise_exception = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Добавление Товара")
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def form_valid(self, form):
#         text = str(self.request.POST.get('title')).lower()
#
#         for letter in az_to_en_for_slug:
#             if letter in text:
#                 text = text.replace(letter, az_to_en_for_slug[letter])
#
#         try:
#             temp_slug = text + "-pk" + str(Tovar.objects.latest('pk').id + 1)
#         except:
#             temp_slug = text + "-pk0"
#
#         temp_slug2 = unidecode(temp_slug)
#
#         form.instance.slug = defaultfilters.slugify(temp_slug2)
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)

@login_required(redirect_field_name="login")
def addtovar(request):
    is_seller_user = auth.get_user(request)
    if is_seller_user.is_seller:
        if request.method == "POST":
            form = AddTovarForm(request.POST, request.FILES)
            cats = Category.objects.all()
            if form.is_valid():

                text = str(request.POST.get('title')).lower()

                for letter in az_to_en_for_slug:
                    if letter in text:
                        text = text.replace(letter, az_to_en_for_slug[letter])

                try:
                    temp_slug = text + "-pk" + str(Tovar.objects.latest('pk').id + 1)
                except:
                    temp_slug = text + "-pk0"

                temp_slug2 = unidecode(temp_slug)

                form.instance.slug = defaultfilters.slugify(temp_slug2)
                form.instance.created_by = request.user
                form.instance.title_small = str(form.instance.title).lower()
                form.instance.content_small = str(form.instance.content).lower()

                form.save()
                return redirect("home")
        else:
            form = AddTovarForm()
        data = {
            'form': form,
            # 'cat': Category.objects.all(),
            'cat': [i.name for i in Category.objects.all()],
            'podcat': PodCat.objects.all(),
            'podpodcat': PodPodCat.objects.all(),
            "title": "Добавление товара"
        }

        return render(request, 'homepage/adding-tovar.html', data)
    else:
        return redirect('login')


def add_tovar_cats(request):
    cat = request.GET.get("cat", None)
    podcat = request.GET.get("podcat", None)
    podpodcat = request.GET.get("podpodcat", None)

    if cat:
        cat = Category.objects.get(id=int(cat))
        podcats = cat.podcat_set.all()
        podcats_list = []
        for i in podcats:
            podcats_list.append([i.id, i.name])
    else:
        podcats_list = []

    if podcat:
        podcat = PodCat.objects.get(id=int(podcat))
        podpodcats = podcat.podpodcat_set.all()
        podpodcats_list = []
        for i in podpodcats:
            podpodcats_list.append([i.id, i.name])
    else:
        podpodcats_list = []

    if podpodcat:
        podpodcat = Tovar.objects.filter(podpodcat_id=int(podpodcat))
        properties = podpodcat[0].properties
        properties = [properties[i][0] for i in properties]
    else:
        properties = []

    response = {
        "podcats": podcats_list,
        "podpodcats": podpodcats_list,
        "properties": properties,
    }

    return JsonResponse(response)


# class ShowTovar(DataMixin, DetailView):
#     model = Tovar
#     template_name = 'homepage/show-tovar.html'
#     slug_url_kwarg = "tovarslug"
#     context_object_name = "tovar"
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title=context['tovar'], cat_selected=context['tovar'].cat_id)
#         return dict(list(context.items()) + list(c_def.items()))


def show_tovar(request, tovarslug):
    cats = Category.objects.all()
    podcats = PodCat.objects.all()
    podpodcats = PodPodCat.objects.all()
    try:
        salesman = auth.get_user(request)
    except:
        salesman = ""
    tovar = get_object_or_404(Tovar, slug=tovarslug)
    store = get_object_or_404(User, email=tovar.created_by)
    tovar.open_times += 1
    tovar.save()

    comments = Rating_andComments.objects.filter(product_id=tovar.id)

    context = {
        'tovar': tovar,
        'title': tovar.title,
        'store': store,
        'cats': cats,
        'pcats': podcats,
        'ppcats': podpodcats,
        'salesman': salesman,
        'comments': comments
    }

    return render(request, 'homepage/show-tovar.html', context=context)


def find_page(request):
    r = request.GET.get("name", None).split()

    cats = Category.objects.all()
    podcats = PodCat.objects.all()
    podpodcats = PodPodCat.objects.all()
    try:
        salesman = auth.get_user(request)
    except:
        salesman = ""

    finder_list_title = "Tovar.objects.filter("
    for i in r:
        finder_list_title += f" , Q(title_small__contains='{i.lower()}')"
    finder_list_title += ")"
    finder_list_title = finder_list_title[:21] + finder_list_title[24:]
    finder_list_title = eval(finder_list_title)

    finder_list_content = "Tovar.objects.filter("
    for i in r:
        finder_list_content += f" , Q(content_small__contains='{i.lower()}')"
    finder_list_content += ")"
    finder_list_content = finder_list_content[:21] + finder_list_content[24:]
    finder_list_content = eval(finder_list_content)

    finder_list_content = [i for i in finder_list_content if i not in finder_list_title]

    context = {
        "list_title": finder_list_title,
        "list_content": finder_list_content,
        'cats': cats,
        'pcats': podcats,
        'ppcats': podpodcats,
        'salesman': salesman,
        'r': " ".join(r),
        'title': f"FindAz - {' '.join(r)}",
    }

    try:
        fav_user = auth.get_user(request)
        fav_tovari = fav_user.user_favorite.all()
        context["salesman"] = fav_user
        context["fav_tovari"] = fav_tovari
        context["cart_tovari"] = fav_user.user_cart.all()
    except:
        context["salesman"] = ""
        context["fav_tovari"] = []
        context["cart_tovari"] = []

    return render(request, "homepage/find_page.html", context)


class HomeCategory(DataMixin, ListView):
    model = Tovar
    template_name = "homepage/filter-index.html"
    context_object_name = "tovari"
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        podcats = PodCat.objects.all()
        podpodcats = PodPodCat.objects.all()

        try:
            fav_user = auth.get_user(self.request)
            fav_tovari = fav_user.user_favorite.all()
            cart_tovari = fav_user.user_cart.all()
            context["salesman"] = fav_user
            context["fav_tovari"] = fav_tovari
            context["cart_tovari"] = cart_tovari
            context["fav_tovari_id_list"] = [i.id for i in fav_tovari]
            context["cart_tovari_id_list"] = [i.id for i in cart_tovari]
        except:
            context["salesman"] = ""
            context["fav_tovari"] = []
            context["cart_tovari"] = []

        list_of_properties = Tovar.objects.filter(podpodcat__slug=self.kwargs['podpodcatslug'])
        goods = [i.properties for i in list_of_properties]
        list_of_properties_temp = {}

        for property in goods[0]:
            list_of_properties_temp[goods[0][property][0]] = list(set([good[property][1] for good in goods if good[property][1]!=None]))

        context["list_of_properties"] = list_of_properties_temp
        context["pcats"] = podcats
        context["ppcats"] = podpodcats

        c_def = self.get_user_context(title="FindAz - Категория - " + str(context['tovari'][0].podpodcat), cat_selected=context["tovari"][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Tovar.objects.filter(podpodcat__slug=self.kwargs['podpodcatslug'])


def in_between(request, catslug):
    cats = Category.objects.all()
    podcats = PodCat.objects.all()
    podpodcats = PodPodCat.objects.all()

    cat = Category.objects.get(slug=catslug)
    list_pc = cat.podcat_set.all()
    tovari = cat.tovar_set.all()

    data = {
        "title": f"FindAz - {cat.name}",
        "cats": cats,
        "pcats": podcats,
        "ppcats": podpodcats,
        "list_pc": list_pc,
        "tovari": tovari
    }

    try:
        fav_user = auth.get_user(request)
        fav_tovari = fav_user.user_favorite.all()
        cart_tovari = fav_user.user_cart.all()
        data["salesman"] = fav_user
        data["fav_tovari"] = fav_tovari
        data["cart_tovari"] = cart_tovari
    except:
        data["salesman"] = ""
        data["fav_tovari"] = []
        data["cart_tovari"] = []

    return render(request, "homepage/between_page.html", data)


def p_in_between(request, podcatslug):
    cats = Category.objects.all()
    podcats = PodCat.objects.all()
    podpodcats = PodPodCat.objects.all()

    pcat = PodCat.objects.get(slug=podcatslug)
    list_pc = pcat.podpodcat_set.all()

    tovari = pcat.tovar_set.all()

    data = {
        "title": f"FindAz - {pcat.name}",
        "cats": cats,
        "pcats": podcats,
        "ppcats": podpodcats,
        "list_pc": list_pc,
        "tovari": tovari
    }

    try:
        fav_user = auth.get_user(request)
        fav_tovari = fav_user.user_favorite.all()
        cart_tovari = fav_user.user_cart.all()
        data["salesman"] = fav_user
        data["fav_tovari"] = fav_tovari
        data["cart_tovari"] = cart_tovari
    except:
        data["salesman"] = ""
        data["fav_tovari"] = []
        data["cart_tovari"] = []

    return render(request, "homepage/p_between_page.html", data)


def filter_of_tovar(request):
    r = request.GET.get("property", None)
    # print(f"\n\n{r}\n\n")
    try:
        r = json.loads(r)
        tovari = "Tovar.objects.filter("

        for i in r:
            for el in r[i]:
                if i.lower() in tovari:
                    tovari += f" | Q(properties__{i.lower()}__1='{el}')"
                else:
                    tovari += f" , Q(properties__{i.lower()}__1='{el}')"
        tovari += ")"
        tovari = tovari[:21] + tovari[24:]
        tovari = eval(tovari)
    except:
        tovari = Tovar.objects.filter(podpodcat__slug=r)

    # print(f"\n\n{tovari}\n\n")
    goods_json = serializers.serialize('json', tovari)
    # print(f"\n\n{goods_json}\n\n")

    return HttpResponse(goods_json, content_type='application/json')


# def show_category(request, catid):
#     tovari = Tovar.objects.filter(cat_id=catid)
#
#     if len(tovari)==0:
#         raise Http404
#
#     context = {
#         'tovari': tovari,
#         'cat_selected': catid,
#         'menu': menu,
#         'title': 'index homepage'
#     }
#     return render(request, 'homepage/home.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'homepage/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        # return redirect('home')
        send_email_for_verify(self.request, user)
        return redirect('confirm_email')


class RegisterSeller(DataMixin, CreateView):
    form_class = RegisterSellerForm
    template_name = 'homepage/for-salers.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация Продавца")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.is_seller = True

        text = str(form.instance.occupation).lower()

        for letter in az_to_en_for_slug:
            if letter in text:
                text = text.replace(letter, az_to_en_for_slug[letter])

        temp_slug = unidecode(text)

        form.instance.place_slug = defaultfilters.slugify(temp_slug)
        form.instance.city = "Baku"
        user = form.save()
        # login(self.request, user)
        # return redirect('home')
        send_email_for_verify(self.request, user)
        return redirect('confirm_email')


# def RegisterUser(request):
#     form = RegisterUserForm()
#
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#
#     context = {'form': form}
#     return render(request, 'homepage/register.html', context)


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'homepage/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound("Нет такой страницы")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    # email_from = settings.EMAIL_HOST_USER
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, "admin@mail.ru", [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form": password_reset_form})


def validate_username(request):
    # Проверка доступности и валидности и заполняемой формы
    email = request.GET.get("email", None)

    response = {
        'is_email': User.objects.filter(email__iexact=email).exists(),
    }

    return JsonResponse(response)


User = get_user_model()


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


@login_required(redirect_field_name="login")
def crud_favorites(request):
    r = request.GET.get("favorite", None)
    r = int(r)
    fav_user = auth.get_user(request)

    response = {}

    if r in [i.id for i in list(fav_user.user_favorite.all())]:
        fav_user.user_favorite.remove(Tovar.objects.get(id=r))
        response["is_favorite"] = False
        response["fav_tovari"] = [i.id for i in fav_user.user_favorite.all()]
    else:
        fav_user.user_favorite.add(Tovar.objects.get(id=r))
        response["is_favorite"] = True
        response["fav_tovari"] = [i.id for i in fav_user.user_favorite.all()]

    return JsonResponse(response)

    # ebat.favorite_posts.remove(Tovar.objects.get(id=1))
    # ebat.favorite_posts.all()

    # goods = User.objects.all()
    # goods_json = serializers.serialize('json', goods)
    #
    # return HttpResponse(goods_json, content_type='application/json')


@login_required(redirect_field_name="login")
def show_favorites(request):
    cats = Category.objects.all()
    podcats = PodCat.objects.all()
    podpodcats = PodPodCat.objects.all()
    fav_user = auth.get_user(request)
    tovari = fav_user.user_favorite.all()
    cart_tovari = fav_user.user_cart.all()

    data = {
        "tovari": tovari,
        "cart_tovari": cart_tovari,
        "cats": cats,
        "pcats": podcats,
        "ppcats": podpodcats,
        "salesman": fav_user,
        "title": "FindAz - Избранные"
    }

    return render(request, 'homepage/izbranniy.html', data)


@login_required(redirect_field_name="login")
def crud_cart(request):
    r = request.GET.get("id", None)
    r = int(r)
    cart_user = auth.get_user(request)

    response = {}

    if r in [i.id for i in list(cart_user.user_cart.all())]:
        cart_user.user_cart.remove(Tovar.objects.get(id=r))
        response["is_in_cart"] = False
        response["cart_tovari"] = [i.id for i in cart_user.user_cart.all()]
    else:
        cart_user.user_cart.add(Tovar.objects.get(id=r))
        response["is_in_cart"] = True
        response["cart_tovari"] = [i.id for i in cart_user.user_cart.all()]

    return JsonResponse(response)


def cart_count(request):
    id = request.GET.get("id", None)
    count = request.GET.get("count", None)
    cart_user = auth.get_user(request)
    try:
        tovar = MyCart.objects.get(product_id=int(id), user_id=cart_user.id)
        tovar.count = int(count)
        # print(count, tovar)
        tovar.save()
    except:
        pass
    return JsonResponse({"ganja": "amir/vaga"})


@login_required(redirect_field_name="login")
def show_cart(request):
    cats = Category.objects.all()
    podcats = PodCat.objects.all()
    podpodcats = PodPodCat.objects.all()
    cart_user = auth.get_user(request)
    # tovari = cart_user.user_cart.all()
    tovari_temp = MyCart.objects.filter(user_id=cart_user.id)
    tovari = []
    for i in tovari_temp:
        tovari.append([i.product, i.count])
    fav_tovari = cart_user.user_favorite.all()

    data = {
        "tovari": tovari,
        "fav_tovari": fav_tovari,
        "cats": cats,
        "pcats": podcats,
        "ppcats": podpodcats,
        "salesman": cart_user,
        "title": "FindAz - Корзина"
    }

    return render(request, 'homepage/cart.html', data)


def find(request):
    r = request.GET.get("value", None).split()

    finder_list_title = "Tovar.objects.filter("
    for i in r:
        finder_list_title += f" , Q(title_small__contains='{i.lower()}')"
    finder_list_title += ")"
    finder_list_title = finder_list_title[:21] + finder_list_title[24:]
    finder_list_title = eval(finder_list_title)

    finder_list_title = [i.title for i in finder_list_title]

    response = {
        "list_title": finder_list_title,
    }

    return JsonResponse(response)


def crud_rating_comments(request):
    rating = request.GET.get("rating", None)
    id_tovar = request.GET.get("id", None)
    comment = request.GET.get("comment", None)
    plus = request.GET.get("plus", None)
    minus = request.GET.get("minus", None)
    user = auth.get_user(request)
    tovar = Tovar.objects.get(id=int(id_tovar))

    user.user_rating_and_comment_for_tovar.add(tovar)

    row = Rating_andComments.objects.get(user_id=user.id, product_id=int(id_tovar))
    row.comment = comment
    row.rating = float(rating)
    try:
        row.plus = plus
    except:
        pass
    try:
        row.minus = minus
    except:
        pass
    row.save()

    try:
        tovar_rating = tovar.rating_andcomments_set.all()
        tovar_rating = round(sum([i.rating for i in tovar_rating])/len(tovar_rating), 1)
        tovar.rating = tovar_rating
        tovar.save()
    except:
        pass

    response = {
        "added": True
    }

    return JsonResponse(response)
