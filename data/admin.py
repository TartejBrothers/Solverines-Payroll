from django.contrib import admin
from .models import *

from import_export.admin import ExportActionMixin


class Databaseadmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [
        "name",
        "id",
        "dept",
        "salary",
        "designation",
        "gender",
        "pan_no",
        "aadhar_no",
        "dateofbirth",
        "dateofjoining",
        "bankname",
        "ac_no",
        "uan_no",
    ]


admin.site.register(Database, Databaseadmin)
