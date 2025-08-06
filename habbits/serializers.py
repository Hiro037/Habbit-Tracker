from rest_framework.serializers import ModelSerializer

from habbits.models import Habbit


class HabbitSerializer(ModelSerializer):
    class Meta:
        model = Habbit
        fields = "__all__"
        read_only_fields = ['user']
