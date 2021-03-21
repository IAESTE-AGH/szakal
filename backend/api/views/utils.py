from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GetStatistics(APIView):
    serializer_class = None


class GetTop10Users(APIView):
    serializer_class = None


class GetCurrentEvent(APIView):
    serializer_class = None