from django.db import models


class Editor(models.Model):
    id = models.BigAutoField(primary_key=True, help_text='에디터 고유 번호')
    name = models.CharField(max_length=100, help_text='이름')
    created_at = models.DateTimeField(auto_now_add=True, help_text='생성일')
    updated_at = models.DateTimeField(auto_now=True, help_text='수정일')

    class Meta:
        ordering = ['-id']
