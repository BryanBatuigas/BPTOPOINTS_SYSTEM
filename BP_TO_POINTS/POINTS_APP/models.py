from random import choices
from turtle import width
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser

class Useraccount(AbstractUser):

    Usertype = [
        ('A', 'Admin'),
        ('S', 'Student'),]

    Usertype = models.CharField(choices = Usertype, max_length = 10, verbose_name = 'Usertype', default='S') 

# Create your models here.
class Rewardshistory(models.Model):
    userr = models.CharField(max_length=200, null=True,verbose_name="User")
    items= models.CharField(max_length=200, null=True,verbose_name="Item")
    quantity = models.CharField(max_length=200, null=True,verbose_name="Quantity")
    totalpoints = models.CharField(max_length=200, null=True,verbose_name="Total Points")
    datetime = models.CharField(max_length=200, null=True, verbose_name="Date time")

class User_Transactionhistory(models.Model):
    th_userr = models.CharField(null=True, max_length=200)
    th_recyclable= models.CharField(null=True, max_length=200)
    th_quantity = models.CharField(null=True, max_length=200)
    th_totalpoints = models.CharField(null=True, max_length=200)
    th_datetime = models.CharField(null=True, max_length=200)

class RewardsQueue(models.Model):
    user = models.CharField(max_length=200, null=True)
    item = models.CharField(max_length=200, null=True)
    quantity = models.IntegerField(null=True)
    tpoints = models.IntegerField(null=True)
    td = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item

class Rewards_Settings(models.Model):
    Product_Name = models.CharField(max_length=200, null=True)
    Stocks = models.IntegerField(null=True)
    Color = models.CharField(max_length=200, null=True)
    Value_Points = models.FloatField(null=True)

    def __str__(self):
        return self.Product_Name

class PaperModel(models.Model):
    weight = models.FloatField(null=True)
    points = models.FloatField(null=True)
    
    def __str__(self):
        return self.weight

class UserPoints(models.Model):
    user1 = models.CharField('User Name', max_length=200, null=True)
    points = models.FloatField(null=True)

    def __int__(self):
        return self.points

class PaperPointsEquivalent(models.Model):
    paper_weight = models.FloatField(null=True)
    paper_points = models.FloatField(null=True)

    def __int__(self):
        return self.paper_weight

class BottlePointsEquivalent(models.Model):
    bottle_count = models.FloatField(null=True)
    bottle_points = models.FloatField(null=True)

    def __int__(self):
        return self.bottle_count

class AdminRewardsHistory(models.Model):
    user1 = models.CharField(null=True, max_length=150)
    item1 = models.CharField(null=True, max_length=150)
    quantity1 = models.IntegerField(null=True)
    totalpoints1 = models.FloatField(null=True)
    timedate1 = models.DateTimeField(auto_now_add=True, null=True)


class AdminTransactionHistory(models.Model):
    user = models.CharField(null=True, max_length=150)
    recyclable = models.CharField(null=True, max_length=150)
    quantity = models.CharField(null=True, max_length=150)
    points = models.CharField(null=True, max_length=150)
    timedate = models.CharField(null=True, max_length=150)

    def __int__(self):
        return self.user

class User_Rewards_History1(models.Model):
    ur_user = models.CharField(max_length=200, null=True,verbose_name="User")
    ur_item = models.CharField(max_length=200, null=True,verbose_name="Item")
    ur_quantity = models.IntegerField(null=True)
    ur_total_points = models.FloatField(null=True)
    ur_date_time = models.DateTimeField(auto_now_add=True)
    ur_status = models.CharField(max_length=200, null=True)

    def __int__(self):
        return self.ur_user

class Admin_Rewards_Queue(models.Model):
    ar_user = models.CharField(max_length=200, null=True,verbose_name="User")
    ar_item = models.CharField(max_length=200, null=True,verbose_name="Item")
    ar_quantity = models.IntegerField(null=True)
    ar_total_points = models.FloatField(null=True)
    ar_date_time = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.ar_user

class Bottle_Counter(models.Model):
    user = models.CharField(null=True, max_length=150)
    count = models.CharField(null=True, max_length=150)
    
class Notification(models.Model):
    notif_bin = models.CharField(max_length=200, null=True)
    notif_message = models.CharField(max_length=200, null=True)
    

    def __int__(self):
        return self.notif_bin
