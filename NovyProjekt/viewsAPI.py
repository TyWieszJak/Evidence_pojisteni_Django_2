from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Pojistenec
from .serializers import PojistenecSerializer
from django.shortcuts import render

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