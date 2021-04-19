from rest_framework.views import APIView


class User(APIView):
    serializer_class = None


class Industry(APIView):
    serializer_class = None


class Company(APIView):
    serializer_class = None


class Event(APIView):
    serializer_class = None


class Statistics(APIView):
    serializer_class = None


class Top10Users(APIView):
    serializer_class = None


class CurrentEvent(APIView):
    serializer_class = None
