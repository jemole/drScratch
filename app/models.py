import datetime
from django.db import models
from django.contrib.auth.models import User

# Models of drScratch

class File(models.Model):
    filename = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, default='drscratch')
    coder = models.CharField(max_length=100, default='drscratch')
    method = models.CharField(max_length=100)
    time = models.DateField(auto_now=False)
    language = models.TextField(default="en")
    score = models.IntegerField()
    abstraction = models.IntegerField()
    parallelization = models.IntegerField()
    logic = models.IntegerField()
    synchronization = models.IntegerField()
    flowControl = models.IntegerField()
    userInteractivity = models.IntegerField()
    dataRepresentation = models.IntegerField()
    spriteNaming = models.IntegerField()
    initialization = models.IntegerField()
    deadCode = models.IntegerField()
    duplicateScript = models.IntegerField()

class CSVs(models.Model):
    filename = models.CharField(max_length=100)
    directory = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, default='drscratch')
    coder = models.CharField(max_length=100, default='drscratch')
    date = models.DateTimeField(default=datetime.datetime.now)

class Coder(User):
    birthmonth = models.CharField(max_length=100)
    birthyear = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    gender_other = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    img = models.ImageField(upload_to="img/", default="app/images/drScratch.png")

class Organization(User):
    hashkey = models.TextField()
    img = models.ImageField(upload_to="img/", default="app/images/drScratch.png")


class OrganizationHash(models.Model):
    hashkey = models.TextField()


class Comment(models.Model):
	user = models.TextField()
	text = models.TextField()
	date = models.DateField()


class Activity(models.Model):
	text = models.TextField()
	date = models.DateField()


class Discuss(models.Model):
    nick = models.TextField()
    date = models.DateTimeField()
    comment = models.TextField()


class Stats(models.Model):
    daily_score = models.TextField()
    basic = models.TextField(default="")
    development = models.TextField(default="")
    master = models.TextField(default="")
    daily_projects = models.TextField(default="")
    parallelism = models.IntegerField(default=int(0))
    abstraction = models.IntegerField(default=int(0))
    logic = models.IntegerField(default=int(0))
    synchronization = models.IntegerField(default=int(0))
    flowControl = models.IntegerField(default=int(0))
    userInteractivity = models.IntegerField(default=int(0))
    dataRepresentation = models.IntegerField(default=int(0))
    deadCode = models.IntegerField(default=int(0))
    duplicateScript = models.IntegerField(default=int(0))
    spriteNaming = models.IntegerField(default=int(0))
    initialization = models.IntegerField(default=int(0))

######################### UNDERDEVELOPMENT ####################################


class Student(models.Model):
    #student = models.ForeignKey(User, unique=True)
    student = models.OneToOneField(User)


class Teacher(models.Model):
    #teacher = models.ForeignKey(User, unique=True)
    teacher = models.OneToOneField(User)
    username = models.TextField()
    password = models.TextField()
    email = models.TextField()
    hashkey = models.TextField()
    #classroom = models.ManyToManyField(Classroom)
