from django.contrib import admin
from . import models

admin.site.register(models.Place)
admin.site.register(models.Category)
admin.site.register(models.MenuItem)
admin.site.register(models.Order)
