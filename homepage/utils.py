from django.db.models import Count
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import *


def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    domain = current_site.domain

    context = {
        'email': user.email,
        'user': user,
        'domain': domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": token_generator.make_token(user),
    }

    message = render_to_string('homepage/verify_email.html', context=context)
    email = EmailMessage('Verify Email', message, to=[user.email])

    email.send()


class DataMixin():
    # paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.annotate(Count('tovar'))
        cats = Category.objects.order_by('id')

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
