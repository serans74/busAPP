from django.contrib import admin

from base.models import Ride, Ticket

admin.site.register(Ticket)


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['bus_company', 'is_express', 'average_speed']
