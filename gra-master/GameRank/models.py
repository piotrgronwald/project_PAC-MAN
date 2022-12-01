from django.db.models import DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField, Model, \
    TextField, CASCADE, OneToOneField
from django.contrib.auth.models import User
from django.db import models
from GameRank.admin import WebAppAdmin


class GameRank1(Model):
    username = ForeignKey(User, to_field="username", on_delete=CASCADE)
    ranking = IntegerField()
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.__dict__)


class Profile(Model):
    username = OneToOneField(User, on_delete=CASCADE)
    clicks_left = IntegerField()



