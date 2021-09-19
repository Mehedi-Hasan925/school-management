from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("email field is required")
        
        email = self.normalize_email(email)
        user =  self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        


        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# create Custom user model to authenticate with email and password instead of default username and apssword
class User(AbstractBaseUser,PermissionsMixin):
    CHOICES = (
    ('Student', 'Student'),
    ('Parent ', 'Parent '),
    ('Teacher', 'Teacher'),
    )

    email = models.EmailField(unique=True, null=False)
    user_type = models.CharField(max_length=7,choices=CHOICES,null=True,blank=False)
    join_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email



# create profile model to store Basic information about user.
class user_info(models.Model):

    GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female ', 'Female '),
    ('Others', 'Others'),
    )
    
    
    # start database
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_info')
    first_name = models.CharField(max_length=264,blank=False,verbose_name='First Name')
    last_name = models.CharField(max_length=264,blank=False, verbose_name='Last Name')
    profile_Image = models.ImageField(upload_to='profile_pics',verbose_name='Profile Image')
    gender = models.CharField(max_length=7,choices=GENDER_CHOICES,null=True,blank=False)
    Country = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=250, blank=False) 
    city = models.CharField(max_length=250, blank=False)
    
    
    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, raw=False, **kwargs):
    if created and not raw:
        user_info.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile_info.save()
    
