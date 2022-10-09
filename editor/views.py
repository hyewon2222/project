from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin

from editor.serializers import CreateEditorSerializer


class AdminEditorView(CreateModelMixin, GenericAPIView):
    serializer_class = CreateEditorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
