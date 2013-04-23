from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


class Person(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.CharField(max_length=100)
    skype = models.CharField(max_length=100)
    other_contacts = models.TextField()
    photo = models.ImageField(
        upload_to='images',
        default='images/default.jpg',
        null=True)

    def __unicode__(self):
        return self.name + " " + self.last_name


class Request(models.Model):
    path = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    user = models.ForeignKey(User, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        return self.method + " " + self.path


class ObjectLog(models.Model):
    model_type = models.ForeignKey(ContentType)
    action = models.CharField(max_length=10)
    time = models.DateTimeField(auto_now=True)
    object_id = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return (str(self.model_type) +
                ' id: ' + str(self.object_id) + ' ' +
                self.action + ' at ' + str(self.time))
