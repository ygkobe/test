from django.db import models
from django.contrib.auth.models import AbstractUser
# from Common.db import BaseModel


class User(AbstractUser):
    """
    用户模型
    """


    class Meta:
        db_table = "user"
        verbose_name = "用户表"
        verbose_name_plural = "用户表"

