from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = 