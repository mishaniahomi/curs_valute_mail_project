from django import template

from curs.models import Valute

register = template.Library()
@register.simple_tag()
def get_valutes():
    return Valute.objects.all()