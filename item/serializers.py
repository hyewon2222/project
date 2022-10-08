from rest_framework.serializers import ModelSerializer, IntegerField, CharField
from rest_framework.exceptions import NotFound

from item.models import Item
from actor.models import Actor


class CreateItemSerializer(ModelSerializer):
    korea_title = CharField(max_length=100, required=True)
    korea_contents = CharField(max_length=5000, required=True)
    price = IntegerField(required=True)
    sale_price = IntegerField(default=0)

    class Meta:
        model = Item
        fields = '__all__'

    def validate(self, attrs):
        actor = Actor.objects.filter(id=attrs['actor_id'].id).first()
        if actor is None:
            raise NotFound('작가정보가 올바르지 않습니다.')
        return attrs

    def create(self, validated_data):
        item = Item.objects.create(**validated_data)
        return item

    class Meta:
        model = Item
        fields = '__all__'
        extra_kwargs = {
            "id": {"read_only": True}
        }