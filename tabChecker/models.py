from datetime import datetime

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, wants_promo=0):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            wants_promo=wants_promo,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user

    def create_customer(self, email, first_name, last_name, phone_number, password, wants_promo, address):
        if not email:
            raise ValueError('Users must have an email address')
        customer = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            wants_promo=wants_promo,
            address=address
            # payment_info = payment_info
        )
        customer.is_active = False
        customer.set_password(password)
        customer.save()
        print(customer.is_active)
        return customer


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=50)
    wants_promo = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name']

    def __str__(self):
        return self.first_name


class Admin(User):
    is_staff = True
    is_admin = True
    is_active = True
    is_superuser = True

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    def __str__(self):
        return super().__str__()


class bar(models.Model):
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    zipCode = models.CharField(max_length=5)
    website = models.URLField(max_length=200, default='')
    logo = models.ImageField()

    def __str__(self):
        return self.name


class Manager(User):
    is_staff = True
    is_active = True
    location = models.ForeignKey(bar, on_delete=models.CASCADE)


class Attendees(models.Model):
    file = models.FileField(upload_to='upload/')

    def __str__(self):
        return f'upload/{self.file}'


class Organizer(User):
    pass


class Organization(models.Model):
    name = models.CharField(max_length=50)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, null=True, )

    def __str__(self):
        return self.name


class Members(models.Model):
    first_name = models.CharField('First Name', max_length=20)
    last_name = models.CharField(max_length=20)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField()
    imported = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class event(models.Model):
    title = models.CharField(max_length=50)
    AttendingOrgs = models.ManyToManyField(Organization)
    location = models.ForeignKey(bar, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} at {self.location}'


class MemberSheetUpload(models.Model):
    description = models.CharField(max_length=200, null=True)
    document = models.FileField(upload_to='upload/', )
    uploaded_at = models.DateField(auto_now_add=True)
