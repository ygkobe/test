# -*- coding:utf8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    用户模型
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('test', 'Test'),
    ]
    role = models.CharField(choices=ROLE_CHOICES, max_length=255, default='user')

    class Meta:
        db_table = "user"
        verbose_name = "用户表"
        verbose_name_plural = "用户表"

