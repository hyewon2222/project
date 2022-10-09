from rest_framework.serializers import ModelSerializer, CharField

from actor.models import Actor


class CreateActorSerializer(ModelSerializer):
    name = CharField(max_length=100)

    class Meta:
        model = Actor
        fields = '__all__'

    def create(self, validated_data):
        actor = Actor.objects.create(**validated_data)
        return actor
    