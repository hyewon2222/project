from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, IntegerField, CharField, FloatField, BooleanField
from rest_framework.exceptions import ValidationError, NotFound

from actor.models import Actor
from editor.models import Editor
from item.models import Item
from utils.exchange_rate import exchange_rate
from utils.translation import translation


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


class AdminUpdateItemCheckSerializer(ModelSerializer):
    status = CharField(max_length=20, required=True)
    commission_rate = FloatField(required=False)
    is_active = BooleanField(required=False)

    class Meta:
        model = Item
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        if instance.commission_rate == 0.0 and \
                validated_data.get('commission_rate') is None and \
                validated_data['status'] == 'success':
            raise ValidationError('수수료를 입력해주세요.')

        editor = Editor.objects.filter(id=validated_data['editor_id'].id).first()
        if editor is None:
            raise NotFound('존재하지 않는 에디터입니다.')

        for key in validated_data:
            setattr(instance, key, validated_data.get(key))

        instance.editor_name = editor.name
        if validated_data['status'] == 'success':
            korea_title = instance.korea_title
            korea_contents = instance.korea_contents
            instance.english_title = translation('en', korea_title)
            instance.english_contents = translation('en', korea_contents)
            instance.china_title = translation('zh-CN', korea_title)
            instance.china_contents = translation('zh-CN', korea_contents)

        instance.save()
        return instance


class AdminItemCheckSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ListItemSerializer(ModelSerializer):
    english_price = SerializerMethodField()
    english_sale_price = SerializerMethodField()
    china_price = SerializerMethodField()
    china_sale_price = SerializerMethodField()
    commission_price = SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'

    def get_english_price(self, obj):
        return round(obj.price / float(self.context['exchange_rate']['english']), 2)

    def get_english_sale_price(self, obj):
        return round(obj.sale_price / float(self.context['exchange_rate']['english']), 2)

    def get_china_price(self, obj):
        return round(obj.price / float(self.context['exchange_rate']['china']), 2)

    def get_china_sale_price(self, obj):
        # rate = exchange_rate()
        return round(obj.sale_price / float(self.context['exchange_rate']['china']), 2)

    def get_commission_price(self, obj):
        return obj.price * obj.commission_rate