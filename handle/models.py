#!/usr/bin/env python
#!_*_coding:utf-8_*_


from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class context(models.Model):
    title = models.CharField(max_length=100)
    auther = models.CharField(max_length=20)
    time = models.DateField()
    details = models.TextField()
    status = models.BooleanField(default=0)



