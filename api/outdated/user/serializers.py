from rest_framework_json_api import serializers

from outdated.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
