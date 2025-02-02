from rest_framework import serializers
from .models import ProductTB, CategoryTB

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTB
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='producttb_set')
    class Meta:
        model = CategoryTB
        fields = ['id', 'name', 'products']
