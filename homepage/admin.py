from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import RegisterUserForm
from .models import *


User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", 'email', "password1", "password2"),
            },
        ),
    )
    add_form = RegisterUserForm


class TovarAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "for_adult")
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {
        "slug": ("name",),
        "topic": ("slug",)
    }


class PodCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {
        "slug": ("name",),
    }


class PodPodCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {
        "slug": ("name",),
    }


admin.site.register(Tovar, TovarAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PodCat, PodCategoryAdmin)
admin.site.register(PodPodCat, PodPodCategoryAdmin)
