import bcrypt
# from black import err
from django.db import models
import re

class EmployeeManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        employee = Employee.objects.filter(email=postData['email'])

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters'

        if len(postData['email']) == 0:
            errors['email'] = "Invalid email address!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"

        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'

        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match'

        if employee:
            errors['employee'] = 'A user with this email already exists'
        return errors

    def login_validator(self, postData):
        errors = {}

        employee = Employee.objects.filter(email=postData['email'])

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['email']) == 0:
            errors['email'] = "Please enter an email address!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email or password"

        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'

        if employee:
            if not bcrypt.checkpw(postData['password'].encode(), employee[0].password.encode()):
                errors['auth'] = 'Invalid email or password'
        elif not employee:
            errors['employee'] = 'No account associated with this email'

        return errors

    def update_password_validator(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'

        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match'
        return errors


class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EmployeeManager()
    
