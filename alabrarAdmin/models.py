from email.policy import default
from unicodedata import name
from django.db import models
import datetime
from djmoney.models.fields import MoneyField
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files import File
import PIL.Image


class Customer(models.Model):
    name = models.CharField(max_length=200)
    customer_id = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=200)
    contact_address = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_created', 'name']


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


    class Meta:
        ordering = ['customer']

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


    class Meta:
        ordering = ['customer']


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


    class Meta:
        ordering = ['customer']


class DesignType(models.Model):
    type_name = models.CharField(max_length=200, null=True)
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )

    def __str__(self):
        return self.type_name


    class Meta:
        ordering = ['type_name']
        
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
    total = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )

    recieved = models.DateTimeField(auto_now_add=True)
    collection_date = models.DateTimeField()
    sms_text = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer)


    class Meta:
        ordering = ['-recieved', '-collection_date']


class JobItem(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    design_type = models.ForeignKey(DesignType, on_delete=models.CASCADE)
    material = models.ImageField(upload_to='materials', null=True)

    def __str__(self):
        return str(self.design_type)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL.Image.open(self.material)
        width, height = img.size
        target_width = 600
        h_coefficient = width/600
        target_height = height/h_coefficient
        img = img.resize((int(target_width), int(target_height)), PIL.Image.ANTIALIAS)
        img.save(self.material.path, quality=100)
        img.close()
        self.material.close()


    class Meta:
        ordering = ['job']




class Staff(models.Model):
    name = models.CharField(max_length=200, null=True)
    staff_number = models.CharField(max_length=200, unique=True, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['name']


    

class StaffWage(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    total_amount = MoneyField(
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


    paid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.staff)


    class Meta:
        ordering = ['-paid_on']

class WorkType(models.Model):
    name = models.CharField(max_length=200, null=True)
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class StaffActivity(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    activitity = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)
    done_on = models.DateTimeField(auto_now_add=True)
    wages_group = models.ForeignKey(StaffWage, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.staff)



    class Meta:
        ordering = ['-done_on']


class Consumables(models.Model):
    item = models.CharField(max_length=200, null=True)
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )

    def __str__(self):
        return self.item


    class Meta:
        ordering = ['item']

class ItemExpenditure(models.Model):
    item = models.ForeignKey(Consumables, on_delete=models.CASCADE)
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )
    incurred_on = models.DateTimeField(auto_now_add=True)
    recieved_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.item)


    class Meta:
        ordering = ['-incurred_on']


class SellsItem(models.Model):
    description = models.CharField(max_length=200, null=True)
    available = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )


    def __str__(self):
        return self.description

class SellItemRestock(models.Model):
    sells_item = models.ForeignKey(SellsItem, on_delete=models.CASCADE, null=True)
    amount_stocked = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )
    stocked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sells_item)

    class Meta:
        ordering = ['-stocked_on']


class Sell(models.Model):
    item = models.ForeignKey(SellsItem, on_delete=models.CASCADE, null=True)
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )
    sold_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item)

    class Meta:
        ordering = ['-sold_on']