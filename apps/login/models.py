from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def validation(self, postData):
        errors=[]
        if len(postData["first_name"])==0:
            errors.append("Please insert Your First name")
        elif len(postData["first_name"])<2:
            errors.append("First Name needs to be 2-45 characters")
        elif not re.search(r'^[A-Za-z]+$', postData["first_name"]):
            errors.append("First name needs to be in alphabets")
        if len(postData["last_name"])==0:
            errors.append("Please insert Your Last Name")
        elif len(postData["last_name"])<2:
            errors.append("Last Name needs to be 2-45 characters")
        elif not re.search(r'^[A-Za-z]+$', postData["last_name"]):
            errors.append("Last name needs to be in alphabets")
        if len(postData["email"])==0:
            errors.append("Please insert an email address in the bracket")
        elif not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', postData["email"]):
            errors.append("Please insert a valid email address")
        elif len(User.objects.filter(email=postData["email"]))>0:
            errors.append("Email is already")
        if len(postData["password"])<8:
            errors.append("Password needs to more than 8 characters")
        if postData["confirm"] != postData["password"]:
            errors.append("Make sure password and confirmation matches!")
        if len(errors)==0:
            user= User.objects.create(first_name=postData["first_name"],last_name=postData["last_name"], email= postData["email"], pw_hash= bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()))
            return(True,user)
        else:
            return(False,errors)

    def authenticate(self, postData):
        if "email"in postData and "password" in postData:
            try:
                # print 80*"*"
                # print 'User.objects.filter(email=postData["email"])', User.objects.get(email=postData["email"])
                user = User.objects.get(email=postData["email"])
                # print "user.pw_hash", user.pw_hash
                # print 80*"*"
            except User.DoesNotExist:
                return (False, "Invalid email /password combination")
        pw_match= bcrypt.hashpw(postData['password'].encode(),user.pw_hash.encode())

        if pw_match == user.pw_hash:
            return(True, user)
        else:
            return (False, "Please enter login Information")

class User(models.Model):
    first_name= models.CharField(max_length=45)
    last_name= models.CharField(max_length=45)
    email= models.CharField(max_length=45)
    pw_hash= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects= UserManager()

class MessageManager(models.Manager):
    def validation(self, postData, id):
        if len(postData["secret"])<1:
            return(False, "Secret cannot be empty field")
        else:
            valid= Message.objects.create(content=postData['secret'], creator=User.objects.get(id=id))
            print "Successfully created Secret"
            return(True, valid)

    def like(self, id, message_id):
        liker= User.objects.get(id=id)
        message= self.get(id=message_id)
        alreadyLiked= User.objects.filter(likers=message, id=id)
        if(len(alreadyLiked)==0):
            message.likes.add(liker)
            return True
        else:
            return False

class Message(models.Model):
    content= models.TextField(max_length=1000)
    creator= models.ForeignKey(User, related_name= "author")
    likes= models.ManyToManyField(User, related_name="likers")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects= MessageManager()
