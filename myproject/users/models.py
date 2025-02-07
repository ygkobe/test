from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    # 在这里可以添加额外的字段，例如手机号、地址等
    phone_number = models.CharField(max_length=15, blank=True)

    class Meta:
        db_table = "users"
