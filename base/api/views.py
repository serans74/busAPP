from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import RideSerializer, RideMiniSerializer, UserMiniSerializer
from base.models import Ride, Ticket
from ..rides_functuins import cities_list


class RideSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserMiniSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['GET'])
    def tickets(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user.is_authenticated and request.user == user:
            query = Ticket.objects.filter(owner=user)
            tickets_list = [str(ticket) for ticket in query]
            price_sum = sum([ticket.bus.price for ticket in query])
            avg_price = price_sum / len(tickets_list)
            context = {'User': user.username,
                       'tickets count': len(tickets_list),
                       'tickets list': tickets_list,
                       'Money spent on tickets': price_sum,
                       'Average ticket cost': avg_price}
            return Response(context)
        else:
            return Response({'Acces': 'Denied'})


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    pagination_class = RideSetPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        ride = self.get_object()
        ride.bus_company = request.data.get('bus_company', ride.bus_company)
        ride.average_speed = request.data.get('average_speed', ride.average_speed)
        ride.cities_where_collect_passengers = request.data.get('cities_where_collect_passengers',
                                                                ride.cities_where_collect_passengers)
        ride.is_express = request.data.get('is_express', ride.is_express)
        ride.price = request.data.get('price', ride.price)
        ride.save()
        serializer = RideSerializer(ride, many=False)
        return Response(serializer.data)

    # Ride objects, which contains city taken from query param in 'bus.cities_where_collect_passengers'
    @action(detail=False, methods=['get'])
    def routes(self, request, *args, **kwargs):
        q = self.request.query_params['city']
        rides = Ride.objects.all()
        list_of_ids = [bus.id for bus in rides if q in bus.cities_where_collect_passengers]
        output = Ride.objects.filter(pk__in=list_of_ids)

        serializer = RideMiniSerializer(output, many=True)
        return Response({serializer.data})


@api_view(['GET'])
def cities(request):
    context = dict(enumerate(cities_list(), start=1))
    return Response(context)
