from django.contrib import admin
from authentication_app import models
# from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.user_info)