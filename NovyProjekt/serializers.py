from rest_framework import serializers
from .models import Uzivatel,Pojistenec,Pojisteni,PojistnaUdalost

class UzivatelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uzivatel
        fields = '__all__'

class PojistenecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pojistenec
        fields = '__all__'

class PojisteniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pojisteni
        fields = '__all__'

class PojistnaUdalostiSerializer(serializers.ModelSerializer):
    class Meta:
        model = PojistnaUdalost