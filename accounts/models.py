from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# Create your models here.


class MyAccountmanger(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("Enter Correct Email id")
        if not username:
            raise ValueError('Must Provide with Valid username ')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        # now cuz we are creating user we need to make this required fields true

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50, unique=True)

    date_join = models.DateTimeField(auto_now_add=True)
    last_login = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    # when we write username ='email' , then we will be able to login with email

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # to operate My Account manager wth MyAccount we need to call the above class
    objects = MyAccountmanger()

    def __str__(self):
        return self.email

    def has_perm(self, permission, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
