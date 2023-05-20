from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from .models import Sensor, Reading
from .serializers import SensorSerializer, ReadingSerializer, SensorDetailSerializer


class SensorViewSet(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorDetailViewSet(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class ReadingViewSet(CreateAPIView):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer

# class SensorListView(APIView):                    # APIView alternative with explicitly defined get/post logic
#     def get(self, request):
#         sensors = Sensor.objects.all()
#         serializer = SensorSerializer(sensors, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = SensorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_201_CREATED)






# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

