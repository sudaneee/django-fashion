from django.db import models
import datetime
from djmoney.models.fields import MoneyField

class Customer(models.Model):
    name = models.CharField(max_length=200)
    customer_id = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=200)
    contact_address = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class KaftanMeasurement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200, unique=True, null=True)
    shoulder = models.CharField(max_length=200, null=True)
    long_hand = models.CharField(max_length=200, null=True)
    short_hand = models.CharField(max_length=200, null=True)
    short_length = models.CharField(max_length=200, null=True)
    jampa_length = models.CharField(max_length=200, null=True)
    full_length = models.CharField(max_length=200, null=True)
    neck = models.CharField(max_length=200, null=True)
    burst = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.customer)


class TrouserMeasurement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200, unique=True, null=True)
    length = models.CharField(max_length=200, null=True)
    waist = models.CharField(max_length=200, null=True)
    hip = models.CharField(max_length=200, null=True)
    thigh = models.CharField(max_length=200, null=True)
    knee = models.CharField(max_length=200, null=True)
    calf = models.CharField(max_length=200, null=True)
    ankle = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.customer)


class SuitMeasurement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200, unique=True, null=True)
    length = models.CharField(max_length=200, null=True)
    shoulder = models.CharField(max_length=200, null=True)
    neck = models.CharField(max_length=200, null=True)
    chest = models.CharField(max_length=200, null=True)
    sleeve = models.CharField(max_length=200, null=True)
    waist = models.CharField(max_length=200, null=True)


    def __str__(self):
        return str(self.customer)


class ShirtMeasurement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200, unique=True, null=True)
    length = models.CharField(max_length=200, null=True)
    shoulder = models.CharField(max_length=200, null=True)
    neck = models.CharField(max_length=200, null=True)
    burst = models.CharField(max_length=200, null=True)
    sleeve = models.CharField(max_length=200, null=True)


    def __str__(self):
        return str(self.customer)


class DesignType(models.Model):
    type_name = models.CharField(max_length=200, null=True)
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )

class Job(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount_charged = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )
    discount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )
    amount_paid = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )
    balance = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )

    recieved = models.DateTimeField(auto_now_add=True)
    collection_date = models.DateTimeField()

    def __str__(self):
        return str(self.customer)


class JobItem(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    design_type = models.CharField(max_length=200, null=True)
    material = models.ImageField(upload_to='materials', null=True)

    def __str__(self):
        return str(self.job)


class Staff(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class StaffWage(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    amount_paid = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )

    job = models.ForeignKey(JobItem, on_delete=models.CASCADE)
    paid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.staff)


class Consumables(models.Model):
    item = models.CharField(max_length=200, null=True)
    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )

    def __str__(self):
        return self.item

class ItemExpenditure(models.Model):
    item = models.ForeignKey(Consumables, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200, null=True)
    incurred_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item)