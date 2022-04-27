from django.contrib import admin
from blogger import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Message)
admin.site.register(models.Background)
admin.site.register(models.Notice)

