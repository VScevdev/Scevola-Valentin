from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def toggle_category_url(context, category):
    request = context['request']
    params = request.GET.copy()

    categories = params.getlist('category')

    if category in categories:
        categories.remove(category)
    else:
        categories.append(category)

    params.setlist('category', categories)

    return f"?{params.urlencode()}"


@register.simple_tag(takes_context=True)
def category_active(context, category):
    request = context['request']
    categories = request.GET.getlist('category')

    return 'is-active' if category in categories else ''