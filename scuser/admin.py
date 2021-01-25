from django.contrib import admin
from .models import Scuser


# Register your models here.

class ScuserAdmin(admin.ModelAdmin):
    list_display = ('email',)


admin.site.register(Scuser, ScuserAdmin)
