from django.db import models
from PIL import Image
from django.utils.html import format_html
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.http.response import HttpResponse

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Email Address Is Required')

        if not username:
            raise ValueError('Please Add A User Name')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,

        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(
        max_length=50, unique=True, verbose_name='User Name')
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, verbose_name='Phone Number')
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, blank=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):

    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profilePicture = models.ImageField(
        upload_to='Images/UserProfile/', verbose_name='Profile Picture', blank=True, null=True)
    addressLine_1 = models.CharField(
        max_length=150, verbose_name='Address Line 1')
    addressLine_2 = models.CharField(
        max_length=150, verbose_name='Address Line 2', blank=True)
    city = models.CharField(max_length=50, verbose_name='City', blank=True)
    state = models.CharField(max_length=50, verbose_name='State', blank=True)
    pincode = models.CharField(
        max_length=10, verbose_name='Pin Code', blank=True)
    country = models.CharField(
        max_length=50, verbose_name='Country', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profilePicture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profilePicture.path)

    def image_tag(self):
        try:
            if self.profilePicture.url is not None:
                return format_html('<img src="{}" height="50" width="50" style="object-fit: contain; border-radius: 50%"/>'.format(self.profilePicture.url))
            else:
                return ""
        except Exception as e:
            return HttpResponse(e)

    def __str__(self):
        return self.user.first_name

    def fullAddress(self):
        return f"{self.addressLine_1} {self.addressLine_2} {self.city} {self.state} {self.country}"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profile'
