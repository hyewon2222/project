from rest_framework.serializers import ModelSerializer, CharField

from editor.models import Editor


class CreateEditorSerializer(ModelSerializer):
    name = CharField(max_length=100)

    class Meta:
        model = Editor
        fields = '__all__'

    def create(self, validated_data):
        editor = Editor.objects.create(**validated_data)
        return editor
