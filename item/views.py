from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.pagination import CursorPagination

from item.serializers import ListItemSerializer, AdminCreateItemSerializer, AdminUpdateItemCheckSerializer, \
    AdminItemCheckSerializer, AdminUpdateItemSerializer
from item.models import Item
from utils.exchange_rate import exchange_rate


class ItemView(ListModelMixin, GenericAPIView):
    serializer_class = ListItemSerializer
    pagination_class = CursorPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('status',)
    page_size = 1
    ordering = ['-id']
    queryset = Item.objects

    def get_queryset(self):
        return Item.objects.filter(status='success', is_active=True, is_deleted=False).all()

    def get(self, request, *args, ** kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(
            self.paginate_queryset(queryset),
            context={'exchange_rate': exchange_rate()},
            many=True
        )
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
            return AdminItemCheckSerializer
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


class AdminItemCheckView(UpdateModelMixin, GenericAPIView):
    serializer_class = AdminUpdateItemCheckSerializer

    def get_object(self):
        return Item.objects.filter(id=self.kwargs['pk']).first()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            raise NotFound('존재하지 않는 상품입니다.')
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'id': self.kwargs['pk']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminItemUpdateView(UpdateModelMixin, GenericAPIView):
    serializer_class = AdminUpdateItemSerializer

    def get_object(self):
        return Item.objects.filter(id=self.kwargs['pk']).first()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)





