from rest_framework.viewsets import ModelViewSet

from outdated.oidc_auth.permissions import is_readonly

from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [is_readonly()]
