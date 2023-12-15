from rest_framework import viewsets
from .models import Aircraft, Flight
from .serializers import AircraftSerializer, FlightSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.filters import SearchFilter

from django.db.models import Count, Sum
from datetime import datetime


# Create your views here.
class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

    @action(detail=True, methods=['get'])
    def flights(self, request, pk=None):
        try:
            aircraft = Aircraft.objects.get(pk=pk)
            flights = Flight.objects.filter(aircraft = aircraft)

            flight_serializer = FlightSerializer(flights, many=True, context={'request':request})

            return Response(flight_serializer.data)
        except Exception as e:
            return Response({
                'message':'Aircraft might not exist!!'
            })


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    filter_backends = [SearchFilter]
    search_fields = ['departure_airport','arrival_airport','departure_datetime']

    @api_view(['POST'])
    def create_flight(request):
        if request.method == 'POST':
            serializer = FlightSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
    
        return Response({"error": "Method not allowed."}, status=405)


    @action(detail=False, methods=['GET'])
    def retrieve_flight_info_report(self, request):
        # Get the time range from request parameters
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')

        if not (start_time and end_time):
            return Response({"error": "Please provide both start_time and end_time."}, status=400)

        # Convert string parameters to datetime objects
        start_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        end_datetime = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')

        # Filter flights within the given time range
        flights_within_range = Flight.objects.filter(departure_datetime__range=[start_datetime, end_datetime])

        # Get departure airports and their respective flight count
        departure_airports_info = (
            flights_within_range.values('departure_airport')
            .annotate(num_flights=Count('departure_airport'))
            .order_by('departure_airport')
        )

        # Get in-flight time for each aircraft within the time range
        aircraft_in_flight_time = (
            flights_within_range.values('aircraft')
            .annotate(total_time=Sum('duration'))
        )

        response_data = {
            "departure_airports_info": list(departure_airports_info),
            "aircraft_in_flight_time": list(aircraft_in_flight_time)
        }

        return Response(response_data, status=200)

