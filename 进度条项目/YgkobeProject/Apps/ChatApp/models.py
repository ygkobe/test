from django.db import models


class ChatMessage(models.Model):
    question = models.TextField(help_text='问题')
    answer = models.TextField(help_text='答案')
    ip = models.CharField(max_length=255, help_text='ip')
    create_time = models.CharField(max_length=255, help_text='创建时间')  # 使用 auto_now_add 自动设置时间

    class Meta:
        db_table = 'history'
