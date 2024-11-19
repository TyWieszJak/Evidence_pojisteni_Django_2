from rest_framework import serializers
from .models import Pojistenec, Pojisteni, PojistnaUdalost, Uzivatel


class PojistenecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pojistenec
        fields = '__all__'

class PojisteniSerializer(serializers.ModelSerializer):
    pojistenec = PojistenecSerializer(read_only=True)
    class Meta:
        model = Pojisteni
        fields = '__all__'

class PojistnaUdalostSerializer(serializers.ModelSerializer):
    pojisteni = PojisteniSerializer(read_only=True)
    class Meta:
        model = PojistnaUdalost
        fields = '__all__'

class UzivatelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Uzivatel
        fields = ('id', 'user', 'is_admin')

class ZapomenuteHesloSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Případná validace e-mailu, např. kontrola existence e-mailu v databázi
        return value