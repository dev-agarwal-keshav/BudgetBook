from django.db import models
from django.contrib.auth.models import User
choice=(
    ('send','send'),
    ('recv','recv')
)
use=(
    ('cash','cash'),
    ('account','account')
)
# Create your models here.

class Balance(models.Model):
    user=models.ForeignKey(User, related_name='balance', on_delete=models.CASCADE)
    cash_bal=models.IntegerField()
    acc_bal=models.IntegerField()

class Transaction(models.Model):
    user = models.ForeignKey(User, related_name='cash', on_delete=models.CASCADE)
    amt=models.IntegerField()
    name=models.CharField(max_length=1000)
    date=models.DateField()
    type=models.CharField(max_length=100, choices=choice)
    desc=models.TextField(blank=True)

class Account_Transaction(models.Model):
    user = models.ForeignKey(User,related_name='account', on_delete=models.CASCADE)
    amt=models.IntegerField()
    name=models.CharField(max_length=1000)
    date=models.DateField()
    type=models.CharField(max_length=100, choices=choice)
    desc=models.TextField(blank=True)

class Debt(models.Model):
    user = models.ForeignKey(User,related_name='debt', on_delete=models.CASCADE)
    amt=models.IntegerField()
    name=models.CharField(max_length=1000)
    date = models.DateField()
    using=models.CharField(max_length=100, choices=use, blank=True)
    paid=models.BooleanField(default=False)
