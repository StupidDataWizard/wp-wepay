from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Payment)
admin.site.register(models.Payment_For_User)