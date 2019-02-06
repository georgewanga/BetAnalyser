from django.contrib import admin
from home.models import Home


class HomeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'match_date']
    class Meta:
        model = Home

admin.site.register(Home, HomeAdmin)
