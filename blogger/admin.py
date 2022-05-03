from django.contrib import admin
from blogger import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Message)
admin.site.register(models.Background)
admin.site.register(models.Notice)
admin.site.register(models.Follow)
admin.site.register(models.Mlikes)
admin.site.register(models.Cikes)
admin.site.register(models.Comment)



