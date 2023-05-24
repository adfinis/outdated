from rest_framework import viewsets

from outdated.user.models import User
from outdated.user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
