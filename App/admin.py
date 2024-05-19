from django.contrib import admin

from .models import Request


class Admin(admin.ModelAdmin):
    pass


admin.site.register(Request, Admin)