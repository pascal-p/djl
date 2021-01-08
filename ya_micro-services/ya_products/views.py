from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ViewSet):

    def list(self, request):               # GET (list of products) /api/products
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):             # POST /api/products
        pass

    def retrieve(self, request, pk=None):  # GET (one specifc product) /api/products/<pk>
        pass

    def update(self, request, pk=None):    # PUT (one specifc product) /api/products/<pk>
        pass

    def destroy(self, request, pk=None):   # DELETE (one specifc product) /api/products/<pk>
        pass
