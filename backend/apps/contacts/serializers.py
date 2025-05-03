from rest_framework import serializers
from .models import Public_Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Public_Contact
        fields = '__all__'
