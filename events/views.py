import io
import segno
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user
from django.core.files.base import ContentFile

from .models import Event, Pass
from .serializers import UserSerializer, EventSerializer, PassSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import EventSerializer
from .models import Event

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def dashboard(request):
    """
    Provides an overview of the user's profile, including events and user-specific events.
    """
    # Get all events
    event_serializer = EventSerializer(Event.objects.all(), many=True)

    # Get events the current user is attending
    my_event_serializer = EventSerializer(Event.objects.filter(attendees=request.user), many=True)

    # Structure the data
    data = {
        'all_events': event_serializer.data,
        'my_events': my_event_serializer.data,
    }

    return Response(data, status.HTTP_200_OK)


@api_view(['POST'])
def pass_create(request, pk):
    '''
    Creates a new pass, genrates and stores the QR code
    '''
    # serializer = PassSerializer(data=request.data)
    # Get the current details
    # if serializer.is_valid():
    #     user = serializer.validated_data['user']
    #     event = serializer.validated_data['event']
    #     pass_status = serializer.validated_data.get('status', 'active')
    #     data = [user.id, user.username]
    try:
        user = get_user(request)
    except Exception as e:
        return Response({'message': f'User not found{e}'}, status=status.HTTP_404_NOT_FOUND)
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'message': f'User not found{e}'}, status=status.HTTP_404_NOT_FOUND)

    if Pass.objects.filter(user=user, event=event).exists():
        return Response({'message': 'Pass already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate QR code
    qr = segno.make_qr(f'{user.id}-{event.id}')
    buff = io.BytesIO()
    qr.save(buff, kind='png', scale=3)
    
    # Save QR code to the database
    pass_instance = Pass(user=user, event=event)
    pass_instance.qrcode.save(
        f'{user.id}_{event.name}.png',
        ContentFile(buff.getvalue()),
        save=True,
    )
    pass_instance.save()

    # Serialize and return the new pass
    response_serializer = PassSerializer(pass_instance)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def event_list_create(request):
    if request.method == 'GET':
        # List all events
        events= Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Create a new event
        serializer =  EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk):

    # Check if the event exists
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # Retrieve the event
        serializer = EventSerializer(event)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Update the event
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Delete the event
        serializer = EventSerializer(event)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)