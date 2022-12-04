# from tkinter.tix import Select

from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as DjangoAuthenticationForm
from django.core.exceptions import ValidationError

from .models import *
from .utils import send_email_for_verify

User = get_user_model()


# class GroupedSelect(Select):
#     def render(self, name, value, attrs=None, choices=()):
#         if value is None: value = ''
#         final_attrs = self.build_attrs(attrs, name=name)
#         output = [format_html('<select{0}>', flatatt(final_attrs))]
#         for index, option_gp in enumerate(self.choices):
#             if index == 0:
#                 option_value = smart_unicode(option_gp[0])
#                 option_label = smart_unicode(option_gp[1])
#                 output.append(u'<option value="%s">%s</option>' %  (escape(option_value), escape(option_label)))
#                 output.append('<optgroup label = "Configuration">')
#             elif index!=0 and index <= len(self.choices):
#                 option_value = smart_unicode(option_gp[0])
#                 option_label = smart_unicode(option_gp[1])
#                 output.append(u'<option value="%s">%s</option>' % (escape(option_value), escape(option_label)))
#         output.append(u'</optgroup>')
#         output.append(u'</select>')
#         return mark_safe('n'.join(output))


class AuthenticationForm(DjangoAuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is not None:
                if not self.user_cache.email_verify:
                    send_email_for_verify(self.request, self.user_cache)
                    raise ValidationError(
                        'Аккаунт не подтвержден проверьте свою почту',
                        code='invalid_login'
                    )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class AddTovarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["cat"].empty_label = "Категория не выбрана"
        # self.fields["podcat"].empty_label = "ПодКатегория не выбрана"
        # self.fields["podpodcat"].empty_label = "ПодПодКатегория не выбрана"

    photo_1 = forms.ImageField(required=False, label="Фото1", widget=forms.FileInput(attrs={
        "id": "forfile2",
        "onchange": "previewFile(this)"
    }))
    photo_2 = forms.ImageField(required=False, label="Фото2", widget=forms.FileInput(attrs={
        "id": "forfile3",
        "onchange": "previewFile(this)"
    }))
    photo_3 = forms.ImageField(required=False, label="Фото3", widget=forms.FileInput(attrs={
        "id": "forfile4",
        "onchange": "previewFile(this)"
    }))
    photo_4 = forms.ImageField(required=False, label="Фото4", widget=forms.FileInput(attrs={
        "id": "forfile5",
        "onchange": "previewFile(this)"
    }))
    photo_5 = forms.ImageField(required=False, label="Фото5", widget=forms.FileInput(attrs={
        "id": "forfile6",
        "onchange": "previewFile(this)"
    }))
    photo_6 = forms.ImageField(required=False, label="Фото6", widget=forms.FileInput(attrs={
        "id": "forfile7",
        "onchange": "previewFile(this)"
    }))
    photo_7 = forms.ImageField(required=False, label="Фото7", widget=forms.FileInput(attrs={
        "id": "forfile8",
        "onchange": "previewFile(this)"
    }))
    photo_8 = forms.ImageField(required=False, label="Фото8", widget=forms.FileInput(attrs={
        "id": "forfile9",
        "onchange": "previewFile(this)"
    }))

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={"id": "kategoriya"}))
    podcat = forms.ModelChoiceField(queryset=PodCat.objects.all(), widget=forms.Select(attrs={"id": "podkategoriya"}))
    podpodcat = forms.ModelChoiceField(queryset=PodPodCat.objects.all(), widget=forms.Select(attrs={"id": "podpodkategoriya"}))

    class Meta:
        model = Tovar
        fields = ["title",
                  "for_adult",
                  "barcode",
                  "brand",
                  "weight",
                  "height",
                  "width",
                  "length",
                  "country_of_origin",
                  "producer",
                  "age_to_use",
                  "expiration_date_for_meal",
                  "expiration_date_for_gadgets",
                  "guarantee_period",
                  "content",
                  "photo_main",
                  "photo_1",
                  "photo_2",
                  "photo_3",
                  "photo_4",
                  "photo_5",
                  "photo_6",
                  "photo_7",
                  "photo_8",
                  "price",
                  "price_with_skidka",
                  "cat",
                  "podcat",
                  "podpodcat",
                  "properties"
                  ]
        widgets = {
            "title": forms.TextInput(),
            "content": forms.Textarea(),
            "for_adult": forms.CheckboxInput(attrs={
                "required": False
            }),
            "photo_main": forms.FileInput(attrs={
                "id": "forfile1",
                "onchange": "previewFile(this)"
            })
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превысила 200 символов')
        return title


class RegisterSellerForm(UserCreationForm):
    first_name = forms.CharField(label="Имя Пользователя", widget=forms.TextInput(attrs={
        "placeholder": "Your Name",
    }))
    last_name = forms.CharField(label="Имя Пользователя", widget=forms.TextInput(attrs={
        "placeholder": "Your Surname",
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        "placeholder": "E-Mail",
    }))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        "placeholder": "Password"
    }))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={
        "placeholder": "Repeat your password"
    }))
    birth_day = forms.DateField(label="Дата рождения", widget=forms.DateInput(attrs={
        "type": "date"
    }))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', widget=forms.NumberInput(attrs={
        "placeholder": "For Example: +994 XX XXX XX XX"
    }))
    occupation = forms.CharField(label="Название магазина", widget=forms.TextInput(attrs={
        "placeholder": "Store name"
    }))
    address_type = forms.CharField(label="Адрес магазина", widget=forms.TextInput(attrs={
        "placeholder": "Address"
    }))
    city = forms.CharField(label="Город", required=False, widget=forms.TextInput(attrs={
        "placeholder": "City",
        "disabled": "True",
        "value": "Baku"
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birth_day', 'phone_number', 'gender', 'occupation', 'address_type', 'city', 'place', 'block_number', 'password1', 'password2']


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label="Имя Пользователя", widget=forms.TextInput(attrs={"placeholder": "Your Name"}))
    last_name = forms.CharField(label="Фамилия Пользователя", widget=forms.TextInput(attrs={"placeholder": "Your Surname"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder": "E-Mail"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={"placeholder": "Repeat your password"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Имя Пользователя", widget=forms.TextInput(attrs={"placeholder": "Log in"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
