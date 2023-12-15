from django.contrib import admin
from .models import Aircraft, Flight
# Register your models here.

class AircraftAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'manufacturer', 'active')
    search_fields = ('serial_number','manufacturer',)
    list_filter = ('active','serial_number','manufacturer',)

class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'aircraft', 'departure_airport', 'arrival_airport', 'duration', 'departure_datetime', 'arrival_datetime')
    search_fields = ('departure_airport', 'arrival_airport',)
    list_filter = ('aircraft', 'departure_airport', 'arrival_airport', 'duration', 'departure_datetime', 'arrival_datetime',)


admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Flight, FlightAdmin)