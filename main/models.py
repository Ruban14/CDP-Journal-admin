from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

PURPOSE_OF_TREES = (
    ('Tender','Tender'),
    ('Neera','Neera'),
    ('Nut','Nut')
)


class User_profile(models.Model):
    name = models.CharField(max_length=50, unique=True)
    street = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    taluk = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    no_of_cocunut_trees = models.IntegerField(blank=True, null=True)
    purpose_of_trees = models.CharField(max_length=25, choices=PURPOSE_OF_TREES,blank=True, null=True)
    phone_number = models.BigIntegerField(unique=True)
    need_print = models.BooleanField(default=False)
    need_online = models.BooleanField(default=False)

    def __str__(self):
        return self.name;

def upload_destination(journal, filename):
    return "main/Journals/{journal}/{date}/{filename}".format(journal=journal.name,date=datetime.datetime.strftime(
                                                                     journal.published_date, "%d-%m-%y"),filename=filename)


class Journals(models.Model):
    name = models.CharField(max_length=250)
    published_date = models.DateField()
    journal_expiry_date = models.DateField()
    published_by = models.ForeignKey(User, blank=True, null=True, related_name='published_by')
    file = models.FileField(upload_to=upload_destination, max_length=1000)
    Thumbnail = models.ImageField(upload_to=upload_destination, max_length=1000)
    time_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name;


# class State(models.Model):
#     name = models.CharField(max_length=50)
#     code = models.CharField(max_length=3)

#     def __str__(self):
#         return self.name


# class District(models.Model):
#     state = models.ForeignKey(State)
#     name = models.CharField(max_length=50)
#     code = models.CharField(max_length=3)
#     capital = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


# class Taluk(models.Model):
#     district = models.ForeignKey(District)
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name








