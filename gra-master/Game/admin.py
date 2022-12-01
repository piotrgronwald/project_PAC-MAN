from django.contrib import admin
from .models import GRA


# admin.site.register(GRA)

@admin.register(GRA)
class AdminGra(admin.ModelAdmin):
    list_display = ['gracz','wynik']
    list_filter = ['gracz']
    search_fields = ['gracz', 'wynik']


# Register your models here.
