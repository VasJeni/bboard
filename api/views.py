from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from main.models import Bb
from .serializers import BbSerializers


@api_view(['GET'])
def bbs(request):
    if request.method == 'GET':
        bbs = Bb.objects.filter(is_active=True)
        serializer = BbSerializers(bbs, many=True)
        return Response(serializer.data)
