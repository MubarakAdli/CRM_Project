from django.db import models

class CustomerManager(models.Manager):
    def customer_validator(self, postData):
        errors = {}
        if len(postData['first']) < 2:
            errors['first'] = 'First Name should be at least 2 characters'
        if len(postData['last']) < 2:
            errors['last'] = 'Last Name should be at least 2 characters'
        if len(postData['city']) < 2:
            errors['city'] = 'City should be at least 2 characters'
        if len(postData['speed'])==0:
            errors['speed'] = 'Please enter a speed'
        return errors

    def update_customer(self, postData):
        errors = {}
        if len(postData['first']) < 2:
            errors['first'] = 'First Name should be at least 2 characters'
        if len(postData['last_name_1']) < 2:
            errors['last'] = 'Last Name should be at least 2 characters'
        if len(postData['city']) < 2:
            errors['city_1'] = 'City should be at least 2 characters'
        return errors

class ServiceManager(models.Manager):
    def service_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = 'Name should be at least 2 characters'

        if len(postData['price'])==0:
            errors['price'] = 'Please enter a price'
        return errors


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    city= models.CharField(max_length=255)
    speed=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomerManager()

class Service(models.Model):
    name = models.CharField(max_length=255)
    price=models.IntegerField()
    customers = models.ManyToManyField(Customer, related_name="services")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ServiceManager()
