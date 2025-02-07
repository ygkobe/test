import os
from django.db import models


class CarNumberInfo(models.Model):
    group_name = models.TextField(help_text='组名')
    car_number = models.TextField(help_text='车牌号')
    create_time = models.TextField( help_text='创建时间')

    class Meta:
        db_table = "car_numbers_group"
