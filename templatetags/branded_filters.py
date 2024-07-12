
from django import template

register = template.Library()

@register.filter(name='as_password')
def as_password(field):
    return field.as_widget(attrs={'type': 'password'})
