from rest_framework.serializers import ModelSerializer, IntegerField, CharField, FloatField, BooleanField
from rest_framework.exceptions import ValidationError, NotFound

from actor.models import Actor
from editor.models import Editor
from item.models import Item
from utils.translation import translation


class ListItemCheckSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class AdminCreateItemSerializer(ModelSerializer):
    korea_title = CharField(max_length=100, required=True)
    korea_contents = CharField(max_length=5000, required=True)
    price = IntegerField(required=True)
    sale_price = IntegerField(default=0)

    class Meta:
        model = Item
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        actor = Actor.objects.filter(id=validated_data['actor_id'].id).first()
        validated_data['actor_name'] = actor.name
        item = Item.objects.create(**validated_data)
        return item
