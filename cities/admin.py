from django.contrib import admin

# Register your models here.
from cities.models import City


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')
    list_display_links = ('pk', 'name')


admin.site.register(City, CityAdmin)
