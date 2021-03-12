import markdown
from django import template

register = template.Library()


@register.filter
def render(value):
    return markdown.markdown(value)
