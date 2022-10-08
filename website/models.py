from audioop import maxpp
from distutils.command.upload import upload
from django.db import models
import datetime
from djmoney.models.fields import MoneyField

class Picture(models.Model):
    tag = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='pictures', null=True)

    def __str__(self):
        return self.tag


class GeneralInformation(models.Model):
    address1 = models.CharField(max_length=200, null=True)
    address2 = models.CharField(max_length=200, null=True)
    phone_no1 = models.CharField(max_length=200, null=True)
    phone_no2 = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.email


class Paragraph(models.Model):
    tag = models.CharField(max_length=200, null=True)
    dummy_text = models.TextField(null=True)

    def __str__(self):
        return self.tag
    


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery', null=True)
    tag = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.tag
    

class Staff(models.Model):
    image = models.ImageField(upload_to='staff', null=True)
    name = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    

class Service(models.Model):
    image = models.ImageField(upload_to='services', null=True)
    tag = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)


    def __str__(self):
        return self.tag


class Blog(models.Model):
    image = models.ImageField(upload_to='services', null=True)
    tag = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.tag

class Shop(models.Model):
    image = models.ImageField(upload_to='services', null=True)
    tag = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )

    def __str__(self):
        return self.tag

class Slider(models.Model):
    image = models.ImageField(upload_to='sliders', null=True)
    tag = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.tag

class ApplicationForms(models.Model):
    description = models.CharField(max_length=200, null=True)
    file_upload = models.FileField(upload_to='forms', null=True)

    def __str__(self):
        return self.description


class Testimonial(models.Model):
    image = models.ImageField(upload_to='services', null=True)
    tag = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)


    def __str__(self):
        return self.tag