from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from .models import Pojistenec
from .serializers import PojistenecSerializer
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes


# Pojistenci

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def seznam_pojistencu(request):
    jmeno = request.GET.get('jmeno','')
    prijmeni = request.GET.get('prijmeni','')
    pojistenci = Pojistenec.objects.filter(jmeno__icontains=jmeno, prijmeni__icontains=prijmeni)

    paginator = Paginator(pojistenci, 10)  # 10 pojištěnců na stránku
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    serializer = PojistenecSerializer(page_obj, many=True)
    return Response({
        'pojistenci': serializer.data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
#@permission_classes([IsAuthenticated])
def smazat_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)
    pojistenec.delete()
    return Response({'message': 'Pojištěnec byl úspěšně smazán.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def detail_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)
    serializer = PojistenecSerializer(pojistenec)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
#@permission_classes([IsAuthenticated])
def upravit_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)
    serializer = PojistenecSerializer(pojistenec, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def pridat_pojistence(request):
    serializer = PojistenecSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
