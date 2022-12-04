from django import template
from homepage.models import *

register = template.Library()


@register.filter(name='index')
def index(arg):
    r = PodCat.objects.all()[arg]
    return r.podpodcat_set.all()[:6]


@register.filter(name='podcatname')
def name(arg):
    r = PodCat.objects.all()[arg]
    return r.name


# @register.simple_tag()
# def get_categories():
#     return Category.objects.all()
#
#
# @register.inclusion_tag("homepage/list_cats.html")
# def show_categories(sort=None, cat_selected=0):
#     if not sort:
#         cats = Category.objects.all()
#     else:
#         cats = Category.objects.order_by(sort)
#     return {"cats": cats, "cat_selected": cat_selected}
