from django.db import models
from actor.models import Actor
from editor.models import Editor


class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    actor_id = models.ForeignKey(Actor, on_delete=models.CASCADE)
    edition_id = models.ForeignKey(Editor, on_delete=models.CASCADE, null=True)
    korea_title = models.CharField(max_length=100, null=False, blank=False)
    korea_contents = models.CharField(max_length=5000, null=False, blank=False)
    english_title = models.CharField(max_length=100, null=True, blank=True)
    english_contents = models.CharField(max_length=5000, null=True, blank=True)
    china_title = models.CharField(max_length=100, null=True, blank=True)
    china_contents = models.CharField(max_length=5000, null=True, blank=True)
    price = models.IntegerField(null=False, blank=False)
    sale_price = models.IntegerField()
    commission_rate = models.FloatField(null=True)
    status = models.CharField(max_length=20, default='ready')
    is_sale = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
