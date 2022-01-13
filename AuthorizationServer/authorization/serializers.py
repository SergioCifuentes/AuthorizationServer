from .models import *
from rest_framework import serializers


class EstadoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Estado_Servidor
        fields = ['estado']

