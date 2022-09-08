from django.contrib import admin
from home.models import Presensi

@admin.register(Presensi)
class PresensiAdmin(admin.ModelAdmin):
    pass