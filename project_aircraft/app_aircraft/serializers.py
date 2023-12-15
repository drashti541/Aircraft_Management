from rest_framework import serializers
from .models import Aircraft, Flight
from django.utils import timezone

class AircraftSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Aircraft
        fields = "__all__"


class FlightSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    duration = serializers.DurationField(read_only=True)

    class Meta:
        model =  Flight
        fields = "__all__"

    def validate(self, data):
        departure_datetime = data['departure_datetime']
        arrival_datetime = data['arrival_datetime']
        existing_flights = Flight.objects.filter(
            departure_airport=data['departure_airport'],
            arrival_airport=data['arrival_airport'],
            departure_datetime=data['departure_datetime'],
            arrival_datetime=data['arrival_datetime']
        )
        

        if departure_datetime <= timezone.now():
            raise serializers.ValidationError("Departure time must be in the future.")

        if arrival_datetime <= departure_datetime:
            raise serializers.ValidationError("Arrival time must be after departure time.")

        if self.instance:  # Exclude current instance if updating
            existing_flights = existing_flights.exclude(pk=self.instance.pk)

        if existing_flights.exists():
            raise serializers.ValidationError("A flight with these airports and times already exists.")

        # Check if the aircraft is already scheduled for another flight at the same time
        aircraft = data['aircraft']
        if Flight.objects.filter(aircraft=aircraft, departure_datetime=data['departure_datetime']).exists():
            raise serializers.ValidationError("This aircraft is already scheduled for another flight at this time.")

        # Calculate duration and add it to the data
        data['duration'] = data['arrival_datetime'] - data['departure_datetime']

        return data

        