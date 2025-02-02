from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CategoryTB, ProductTB
from .serializers import CategorySerializer, ProductSerializer
import os
from django.core.files.storage import default_storage
from django.conf import settings
import numpy as np
import cv2

# Category Views
@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = CategoryTB.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try:
        category = CategoryTB.objects.get(pk=pk)
    except CategoryTB.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response({"message": "Category deleted successful"}, status=status.HTTP_204_NO_CONTENT)

# Products Views
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = ProductTB.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        image = request.FILES.get('image', None)
        if image:
            upload_dir = 'product_images/'
            file_name = default_storage.get_available_name(image.name)
            file_path = os.path.join(upload_dir, file_name)
            default_storage.save(file_path, image)

            request.data['image'] = file_name

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = ProductTB.objects.get(pk=pk)
    except ProductTB.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        image = request.FILES.get('image', None)
        if image:
            upload_dir = 'product_images/'
            file_name = default_storage.get_available_name(image.name)
            file_path = os.path.join(upload_dir, file_name)
            default_storage.save(file_path, image)

            request.data['image'] = file_name

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({"message": "Product deleted successful"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def search_products_by_image(request):
    uploaded_file = request.FILES.get('image')
    if not uploaded_file:
        return Response({"error": "Please upload an image."}, status=status.HTTP_400_BAD_REQUEST)