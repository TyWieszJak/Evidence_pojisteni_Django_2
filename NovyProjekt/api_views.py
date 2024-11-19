from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PojistenecSerializer, PojisteniSerializer, PojistnaUdalostSerializer
from .models import Pojistenec, Pojisteni, PojistnaUdalost

# Seznam a vytváření pojištěnců (GET, POST)
class PojistenecListCreate(APIView):
    def get(self, request):
        pojistenci = Pojistenec.objects.all()
        serializer = PojistenecSerializer(pojistenci, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PojistenecSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Detail pojištěnce (GET, PUT, DELETE)
class PojistenecDetail(APIView):
    def get_object(self, pk):
        try:
            return Pojistenec.objects.get(pk=pk)
        except Pojistenec.DoesNotExist:
            return None

    def get(self, request, pk):
        pojistenec = self.get_object(pk)
        if pojistenec is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PojistenecSerializer(pojistenec)
        return Response(serializer.data)

    def put(self, request, pk):
        pojistenec = self.get_object(pk)
        if pojistenec is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PojistenecSerializer(pojistenec, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pojistenec = self.get_object(pk)
        if pojistenec is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        pojistenec.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Seznam pojištění (GET, POST)
class PojisteniListCreate(ListCreateAPIView):
    queryset = Pojisteni.objects.all()
    serializer_class = PojisteniSerializer

# Detail pojištění (GET, PUT, DELETE)
class PojisteniDetail(RetrieveUpdateDestroyAPIView):
    queryset = Pojisteni.objects.all()
    serializer_class = PojisteniSerializer

# Seznam pojistných událostí (GET, POST)
class PojistnaUdalostListCreate(ListCreateAPIView):
    queryset = PojistnaUdalost.objects.all()
    serializer_class = PojistnaUdalostSerializer

# Detail pojistné události (GET, PUT, DELETE)
class PojistnaUdalostDetail(RetrieveUpdateDestroyAPIView):
    queryset = PojistnaUdalost.objects.all()
    serializer_class = PojistnaUdalostSerializer
