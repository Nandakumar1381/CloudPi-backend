from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Locked
from .serializers import LockedSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework import status
import os

class LockedSendOTPView(APIView):
    def post(self, request):
        User = get_user_model()
        user = User.objects.first()
        #user = request.user
        mail = user.email
 

        otp = get_random_string(length=6, allowed_chars='0123456789')

        locked = Locked(user=user, mail=mail, otp=otp)
        locked.save()

        subject = 'OTP Verification'
        message = f'Your OTP is: {otp}'

        send_mail(
            subject,
            message,
            'cloudpi.2023.secure@gmail.com',  
            [mail],
            fail_silently=False,
            auth_user='cloudpi.2023.secure@gmail.com',  
            auth_password='ypmipfxwadtmoiik',  
            connection=None,
            html_message=None
        )

        return Response({'detail': 'OTP sent successfully'})

class LockedVerifyOTPView(APIView):
    def post(self, request):
        User = get_user_model()
        user = User.objects.first()
        #user = request.user
        otp = request.data.get('otp')
        try:
            locked = Locked.objects.get(user=user, otp=otp)
        except Locked.DoesNotExist:
            return Response({'detail': 'Invalid OTP'})

        return Response({'detail': 'OTP verified successfully'})
    
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def locked_view_upload(request):
    if request.method == 'GET':
        locked = Locked.objects.all()
        serializer = LockedSerializer(locked, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LockedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':  # New section to handle viewing a specific document
        locked_id = request.data.get('locked_id')
        if locked_id:
            try:
                locked = Locked.objects.get(id=locked_id)
                # Perform any additional operations you need with the document
                # For example, you can return the document data or redirect to a download URL
                serializer = LockedSerializer(locked)
                return Response(serializer.data)
            except Locked.DoesNotExist:
                return Response({'error': 'lockedfile not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Missing lockedfile_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['DELETE'])
def locked_delete(request, pk):
    try:
        locked = Locked.objects.get(pk=pk)
    except Locked.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        is_starred = locked.is_starred
        file_path=locked.file.path
        #print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        locked.delete()


        return Response(status=status.HTTP_204_NO_CONTENT)
    


        