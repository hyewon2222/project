from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.pagination import CursorPagination

from item.serializers import ListItemSerializer, AdminCreateItemSerializer, AdminUpdateItemCheckSerializer, \
    AdminItemCheckSerializer
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
        return Item.objects.filter(status='success').all()

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
    # 에디터가 검수할때
    # editor_id가져와서 edirot인지 확인
    # reject이면 item에 reject update 수정 check_item reject 수정
    # success면 item에 success와 check_item data update 하고 check item success 수정
    serializer_class = AdminUpdateItemCheckSerializer

    def get_object(self):
        return Item.objects.filter(id=self.kwargs['pk']).first()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminItemUpdateView(UpdateModelMixin, GenericAPIView):
    # 작가가 수정할때
    # action_id를 받아와서
    # 받아온 값에 있는지 체크하고
    # 수정한다음에 check_item insert하고 item에 ready update
    serializer_class = AdminUpdateItemCheckSerializer

    def get_object(self):
        return Item.objects.filter(id=self.kwargs['pk'], actor_id=1).first()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)





