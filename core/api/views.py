from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import parsers, status, generics
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings

from core.api.serializers import UserCreateSerializer, UserLoginSerializer, PhotoUploadSerializer, FlightSerializer, \
    TicketSerializer
from core.models import Ticket, Flight
from core.tasks import send_initial_ticket_email_task
from core.utils import get_single_object
from airtech.settings import DEFAULT_IMAGE

User = get_user_model()


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def check_flight_status(request, pk):
    """
    Returns the status of a flight
    :param request:
    :param pk:
    :return:
    """
    flight = Flight.objects.get(pk=pk)
    return Response({'status': flight.status}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def check_flight_reservations(request):
    """
    Computes and returns the number of reservations for a flight on a particular day
    :param request:
    :return:
    """
    date = request.data['date']
    day = date.split('-')[2]
    flight_number = request.data['flight_number']
    reservations = Ticket.objects.filter(
        flight_details__flight_number__exact=flight_number, date_created__day=day).count()
    return Response({'reservations': reservations}, status=status.HTTP_200_OK)


class UserCreate(APIView):
    """
    Creates a new user
    :param
    :return
    """
    permission_classes = []

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            user = serializer.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            data = {
                'user': serializer.data,
                'token': token
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    Implements User Login
    """
    permission_classes = []

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoUpdateDestroy(APIView):
    """
    Handles Photo Upload (and Update) and Deletion.
    Since photo upload is handled separately from when a user is created, uploading and
    updating will be a PUT
    """
    permission_classes = [IsAuthenticated, ]

    def put(self, request, pk, format=None):
        parser_classes = (parsers.MultiPartParser, parsers.FormParser)
        user = get_single_object(pk, User)
        if user is not None:
            serializer = PhotoUploadSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = get_single_object(pk, User)
        if user is not None:
            setattr(user, 'photo', DEFAULT_IMAGE)
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FlightList(generics.ListCreateAPIView):
    """
    Create New Flight or List Existing Flights
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated, ]


class FlightDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or Destroy a given flight
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated, ]


class TicketList(generics.ListCreateAPIView):
    """
    Create New Ticket or List Existing Tickets.
    Send email to user with newly created ticket
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        ticket = serializer.save()
        kwargs = {
            "departure_city": ticket.flight_details.depature_city,
            "departure_time": ticket.flight_details.depature_time,
            "departure_date": ticket.flight_details.depature_date,
            "arrival_city": ticket.flight_details.arrival_city,
            "arrival_time": ticket.flight_details.arrival_time,
            "arrival_date": ticket.flight_details.arrival_date,
            "email": ticket.owner.email
        }
        send_initial_ticket_email_task.delay(**kwargs)


class TicketDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or Destroy a given flight
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, ]
