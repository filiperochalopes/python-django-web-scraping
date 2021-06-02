from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from app.core.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def scraping_dentalspeed(request, query):
    # https://www.dentalspeed.com/buscar?palavra=elastioc e
    print(query)
    return Response({"message": "Hello, world!"})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def scraping_dentalcremer(request, query):
    # https://www.dentalcremer.com.br/chaordic/search/result/?origin=autocomplete&ranking=1&terms=+elastico&apikey=dentalcremer-v8&topsearch=1&q=elastico.
    print(query)
    return Response({"message": "Hello, world!"})