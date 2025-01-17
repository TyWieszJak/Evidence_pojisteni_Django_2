from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from .models import Pojistenec
from .serializers import PojistenecSerializer
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view


class PojistenciListAPIView(APIView):
    def get(self, request):
        pojistenci = Pojistenec.objects.all().order_by('jmeno', 'prijmeni')
        jmeno = request.GET.get('jmeno', '')
        prijmeni = request.GET.get('prijmeni', '')

        if jmeno or prijmeni:
            pojistenci = pojistenci.filter(jmeno__icontains=jmeno, prijmeni__icontains=prijmeni)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(pojistenci, request)

        serializer = PojistenecSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['DELETE'])
def smazat_pojistence(request, pk):
    try:
        pojistenec = Pojistenec.objects.get(Pojistenec, pk=pk)
    except Pojistenec.DoesNotExist:
        return Response({'error': 'Pojištěnec nenalezen'}, status=status.HTTP_404_NOT_FOUND)
    pojistenec.delete()
    return Response({'message': 'Pojištěnec byl úspěšně smazán.'}, status=status.HTTP_204_NO_CONTENT)