from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GeoPin, PinMemo
from .serializers import PinCreateSerializer,MemoCreateSerializer,PinOutputSerializer,MemoOutputSerializer
from .utils import haversine_distance

class PinDropView(APIView):
    def post(self, request):
        serializer = PinCreateSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            pin = serializer.save()
            return Response(PinOutputSerializer(pin).data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MemoDropView(APIView):
    def post(self, request):
        serializer = MemoCreateSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            memo = serializer.save()
            return Response(MemoOutputSerializer(memo).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PinProximityView(APIView):
    def get(self, request):
        lat = request.query_params.get('latitude')
        lon = request.query_params.get('longitude')
        radius = request.query_params.get('radius')
        if not all([lat, lon, radius]):
            return Response({"ошибка": "необходимы параметры: latitude, longitude, radius"}, status=400)
        try:
            lat, lon, radius = float(lat), float(lon), float(radius)
        except ValueError:
            return Response({"ошибка": "неверно введён формат параметров"}, status=400)
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180) or radius <= 0:
            return Response({"ошибка": "неверно введены координаты или радиус"}, status=400)
        nearby = [
            p for p in GeoPin.objects.all()
            if haversine_distance(lat, lon, p.latitude, p.longitude) <= radius
        ]
        return Response(PinOutputSerializer(nearby, many=True).data)

class MemoProximityView(APIView):
    def get(self, request):
        lat = request.query_params.get('latitude')
        lon = request.query_params.get('longitude')
        radius = request.query_params.get('radius')
        if not all([lat, lon, radius]):
            return Response({"ошибка": "необходимы параметры: latitude, longitude, radius"}, status=400)
        try:
            lat, lon, radius = float(lat), float(lon), float(radius)
        except ValueError:
            return Response({"ошибка": "неверно введён формат параметров"}, status=400)
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180) or radius <= 0:
            return Response({"ошибка": "неверно введены координаты или радиус"}, status=400)
        nearby_pins = [
            p for p in GeoPin.objects.all()
            if haversine_distance(lat, lon, p.latitude, p.longitude) <= radius
        ]
        memos = PinMemo.objects.filter(pin_id__in=[p.id for p in nearby_pins])
        return Response(MemoOutputSerializer(memos, many=True).data)
