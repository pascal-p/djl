from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework  import status
from rest_framework.views  import APIView
# from django.views.decorators.csrf import csrf_exempt

from .models import Article
from .serializers import ArticleSerializer


class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):

    def get(self, request, id):
        article = self._get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, id):
        article = self._get_object(id)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self._get_object(id)
        article.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    def _get_object(self, id):
        try:
            return Article.objects.get(pk=id)

        except Article.DoesNotExist:
           return HttpResponse(status=status.HTTP_404_NOT_FOUND)
