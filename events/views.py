import io
import segno
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user
from django.core.files.base import ContentFile

from .models import Event, Pass
# from .utils import generate_qr_code
from .serializer import UserSerializer


@api_view(['GET', 'POST'])
def get_pass(request):
    # Get the current logged-in user details
    if request.method == 'POST':
        user = get_user(request)
        data = [user.id, user.username]

        # Generate QR code
        qr = segno.make_qr(data)
        buff = io.BytesIO()
        qr.save(buff, kind='png', scale=3)
        
        # Save QR code to the database
        pass_instance = Pass(user=user)
        pass_instance.event = Event.objects.get(id=1)
        pass_instance.qrcode.save(
            data[1] + '.png',
            ContentFile(buff.getvalue()),
            save=True,
            )

        return Response({'status': 'success'})
    return Response()