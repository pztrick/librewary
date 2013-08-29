import inspect
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import core.models
from core.models import Brewer

for x in dir(core.models):
    obj = getattr(core.models, x)  # x is a string, we must get the object
    if obj == Brewer:
        admin.site.register(Brewer, UserAdmin)
    elif inspect.isclass(obj):
        try:
            admin.site.register(obj)  # we assume that the only class-type objects in models.py are in fact models
        except:
            pass  # we also nest it in a try/except statement to silently ignore any non-model classes which fail to register
