from rest_framework import viewsets,status,permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Criminal, Crime, Arrest, CaseFile
from .serializers import CriminalSerializer, CrimeSerializer, ArrestSerializer, CaseFileSerializer
from .permissions import IsAdminUserOrReadOnly
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email':user.email if hasattr(user,'email') else '',
            'is_admin':user.is_staff if hasattr(user,'is_staff') else False,
        },
            status=status.HTTP_200_OK
        )

class CriminalViewSet(viewsets.ModelViewSet):
    queryset = Criminal.objects.all()
    serializer_class = CriminalSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
class CrimeViewSet(viewsets.ModelViewSet):
    queryset = Crime.objects.all()
    serializer_class = CrimeSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class ArrestViewSet(viewsets.ModelViewSet):
    queryset = Arrest.objects.all()
    serializer_class = ArrestSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class CaseFileViewSet(viewsets.ModelViewSet):
    queryset = CaseFile.objects.all()
    serializer_class = CaseFileSerializer
    permission_classes = [IsAdminUserOrReadOnly]