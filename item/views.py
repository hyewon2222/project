from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.pagination import CursorPagination

from item.serializers import ListItemCheckSerializer, AdminCreateItemSerializer
from item.models import Item


class ItemView(ListModelMixin, GenericAPIView):
    serializer_class = ListItemCheckSerializer
    pagination_class = CursorPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('status',)
    page_size = 1
    ordering = ['-id']
    queryset = Item.objects

    def get_queryset(self):
        a = Item.objects.all()
        return Item.objects.filter(status='success').all()

    def get(self, request, *args, ** kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        return self.get_paginated_response(serializer.data)


class AdminItemView(CreateModelMixin, ListModelMixin, GenericAPIView):
    pagination_class = CursorPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('status',)
    page_size = 1
    ordering = ['-id']
    queryset = Item.objects

    def get_queryset(self):
        return Item.objects.filter(status='ready').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListItemCheckSerializer
        return AdminCreateItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def get(self, request, *args, ** kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        return self.get_paginated_response(serializer.data)




