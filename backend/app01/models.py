from datetime import datetime, timedelta
from symtable import Class

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class StatusChoices(models.IntegerChoices):
    EXAMINE=0  # 审核中
    WORKING=1  # 工作中
    STOP=2 #暂停营业


class Merchant(models.Model):
    merchant_id = models.AutoField(primary_key=True)
    merchant_name = models.CharField(max_length=100,unique=True)
    address = models.CharField(max_length = 100)
    contact_phone  = models.CharField(max_length = 20)
    contact_email = models.EmailField()
    business_hours = models.CharField(max_length = 50)
    logo = models.URLField()
    introduction = models.CharField(max_length = 200)
    avg_score = models.FloatField()
    status = models.IntegerField(choices=StatusChoices.choices,default = 0)
    create_time = models.DateTimeField(auto_now_add=True)
    category_id = models.ForeignKey('Category',on_delete=models.CASCADE)

class Dish(models.Model):
    dish_id = models.AutoField(primary_key=True)
    dish_name = models.CharField(max_length=100)
    description = models.CharField(max_length = 200)
    price = models.FloatField()
    image_url = models.URLField()
    sales_count = models.IntegerField()
    merchant_id = models.ForeignKey('Merchant',on_delete=models.CASCADE)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

class Comment(models.Model):
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    comment_id = models.AutoField(primary_key=True)
    content = models.TextField()
    score = models.IntegerField(choices=SCORE_CHOICES)
    service_score = models.IntegerField(choices=SCORE_CHOICES)
    create_time = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False) # 是否为消费后评价
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    merchant_id = models.ForeignKey('Merchant',on_delete=models.CASCADE)
    dish_id = models.ForeignKey('Dish',on_delete=models.CASCADE,null=True,blank=True)

class RecommendationLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    recommend_time = models.DateTimeField()
    algorithm_type = models.IntegerField()
    parameters = models.JSONField()
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    merchant_ids = models.ManyToManyField('Merchant')






