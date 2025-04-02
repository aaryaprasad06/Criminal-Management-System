from rest_framework import serializers
from .models import Criminal, Crime, Arrest, CaseFile


class CriminalSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Criminal
        fields = '__all__'

class CrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crime
        fields = '__all__'

class ArrestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrest
        fields = '__all__'

class CaseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseFile
        fields = '__all__'
