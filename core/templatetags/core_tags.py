from django import template
from django.conf import settings

register = template.Library()


# settings value
@register.simple_tag
def settings_value(key):
    return getattr(settings, key, "")


#@register.simple_tag
#def external(url, label):
#    return """<a href="%s" target="_blank">%s</a>""" % (url, label)
