from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from base.models import Ride, Ticket


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['holder', 'bus_credentials', 'bought']


class RideSerializer(ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'bus_company', 'average_speed', 'cities', 'is_express',
                  'price', 'cities_where_collect_passengers']

        extra_kwargs = {'cities_where_collect_passengers': {'required': True, 'write_only': True}}


class UserSerializer(ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'tickets']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RideMiniSerializer(ModelSerializer):
    class Meta:
        model = Ride
        fields = ['bus_company', 'cities', 'is_express', 'price']


class UserMiniSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
