from django.contrib import admin
from .models import *

from import_export.admin import ExportActionMixin


class Valueadmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["name", "id", "dept", "email", "phone", "salary"]


admin.site.register(Values, Valueadmin)
