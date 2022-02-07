from django.contrib import admin
from .models import Star
# Register your models here.

#admin.site.register(Star)
@admin.register(Star)
class StarModel(admin.ModelAdmin):
    list_filter = ('star_id','author')
    list_display = ('star_id','author')
