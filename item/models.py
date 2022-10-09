from django.db import models
from actor.models import Actor
from editor.models import Editor


class Item(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='상품 고유 번호')
    actor_id = models.ForeignKey(Actor, on_delete=models.CASCADE, help_text='작가 고유 번호')
    actor_name = models.CharField(max_length=100, null=True, help_text='작가 이름')
    editor_id = models.ForeignKey(Editor, on_delete=models.CASCADE, null=True, help_text='에디터 고유 번호')
    editor_name = models.CharField(max_length=100, null=True, help_text='에디터 이름')
    korea_title = models.CharField(max_length=100, null=False, blank=False, help_text='한국어 상품 제목')
    korea_contents = models.CharField(max_length=5000, null=False, blank=False, help_text='한국어 상품 정보')
    english_title = models.CharField(max_length=100, null=True, blank=True, help_text='영어 상품 제목')
    english_contents = models.CharField(max_length=5000, null=True, blank=True, help_text='영어 상품 정보')
    china_title = models.CharField(max_length=100, null=True, blank=True, help_text='중국 상품 제목')
    china_contents = models.CharField(max_length=5000, null=True, blank=True, help_text='중국 상품 정보')
    price = models.IntegerField(null=False, blank=False, help_text='상품 금액')
    sale_price = models.IntegerField(help_text='세일 상품 금액')
    commission_rate = models.FloatField(null=True, help_text='수수료')
    status = models.CharField(max_length=20, default='ready', help_text='상품 상태')
    is_active = models.BooleanField(default=False, help_text='상품 활성화 여부')
    is_deleted = models.BooleanField(default=False, help_text='상품 삭제 여부')
    created_at = models.DateTimeField(auto_now_add=True, help_text='생성 날짜')
    updated_at = models.DateTimeField(auto_now=True, help_text='수정 날짜')

    class Meta:
        ordering = ['-id']
