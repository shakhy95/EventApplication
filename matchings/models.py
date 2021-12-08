from django.contrib.auth.models import User
from django.db import models
import datetime


class Hobby(models.Model):
    hobby = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.hobby

    # returns a list of all hobbies
    @staticmethod
    def getList():
        return list(Hobby.objects.all())

    # return a hobby object by hobby identifier
    @staticmethod
    def getHobby(hobby):
        return Hobby.objects.get(hobby=hobby)

class Member(User):
    gender = models.CharField(max_length=6, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to='profile_images', null=True, blank=True)
    hobby = models.ManyToManyField(to=Hobby, blank=True, symmetrical=False)

    # return all hobbies of the user
    def getlAllHobbies(self):
        return self.hobby.all()

    # adds the hobby to the user's hobbies
    def addHobby(self, hobby):
        self.hobby.add(Hobby.getHobby(hobby=hobby))

    # removes the hobby from the user's hobbies
    def removeHobby(self, hobby):
        self.hobby.remove(hobby)

    # returns a set of all Member having the hobby
    @staticmethod
    def getAllUserByHobby(hobby):
        return set(Member.objects.filter(hobby=hobby))

    # get all members
    @staticmethod
    def getAllMembers():
        return Member.objects.all()

class Message(models.Model):
    sender = models.ForeignKey(Member, related_name="msg_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Member, related_name="msg_receiver", on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField()

class Event(models.Model):
    owner = models.ForeignKey(Member, related_name="evt-owner+", on_delete=models.CASCADE)
    location = models.CharField(max_length=128, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=128, unique=True)
    desc = models.TextField()
    public = models.BooleanField(default=False)
    participants = models.ManyToManyField(to=Member, related_name="evt-participants+", blank=True, symmetrical=False)

    # add user to the participants' list
    def addParticipant(self, user):
        self.participants.add(user)

    # get all participants
    def getAllParticipants(self):
        return self.participants.all()

    # get event by Title
    @staticmethod
    def getEventByTitle(title):
        return Event.objects.get(title=title)

    # get all events of owner
    @staticmethod
    def getAllEventOf(user):
        return Event.objects.filter(owner=user)
