from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import EmailValidator
import uuid

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, phone_number, fullname, password, **other_fields):
        """
        Create and return a superuser with the given email, phone_number, first_name, last_name, and password.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.')

        user = self.create_user(email, phone_number, fullname, password, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone_number, fullname, password, **other_fields):
        """
        Create and return a regular user with the given email, phone_number first_name, last_name, and password.
        """
        if not email:
            raise ValueError(_('You must provide an email address'))
            
        other_fields.setdefault('is_active', True)

        user_id_prefix = 'ansa'
        user_id_suffix = uuid.uuid4().hex[:8]  # Generate 8-character random suffix

        if password is not None:
            user = self.model(
                email=self.normalize_email(email),
                phone_number=phone_number, fullname=fullname,
                user_id=f'{user_id_prefix}{user_id_suffix}', password=password, **other_fields
            )
            user.save(using=self._db)
        
        else:
            user = self.model(
                email=self.normalize_email(email),
                phone_number=phone_number, fullname=fullname,
                user_id=f'{user_id_prefix}{user_id_suffix}', password=password, **other_fields
            )
            user.set_unusable_password(password)
            user.save(using=self._db)
        
        return user


GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

# Setting profile picture path
def get_profile_image_filepath(self, filename):
    return 'profile_pictures/' + str(self.pk) + '/profile_image.png'

# getting default profile picture
def get_default_profile_picture(gender):
    if gender == 'male':
        return 'default_profile/male.jpg'
    else:
        return 'default_profile/female.jpg'

class AnsaaUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user.
    """
    user_id = models.CharField(max_length=16, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = PhoneNumberField(null=False, blank=True, unique=True)
    fullname = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    gender = models.TextField(choices=GENDER_CHOICES, null=True, blank=True)
    picture = models.ImageField(upload_to=get_profile_image_filepath, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    # zones = models.ManyToManyField('Zones', through='UserZone', related_name='users')

    def save(self, *args, **kwargs):
        if not self.picture:  # If no picture is provided
            self.picture = get_default_profile_picture(self.gender)
        
        if not self.user_id:  # Generate user ID only if not already set
            user_id_prefix = 'ansa'
            user_id_suffix = uuid.uuid4().hex[:6]
            self.user_id = f'{user_id_prefix}{user_id_suffix}'
        super().save(*args, **kwargs)


    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'fullname']

    class Meta:
        ordering = ['-start_date']
        verbose_name = _('Ansa User')
        verbose_name_plural = _('Ansa Users')

    def __str__(self):
        return self.fullname




class OTP(models.Model):
    email = models.EmailField(blank=True, unique=True)
    phone_number = PhoneNumberField(null=False, unique=True, blank=True)
    otp = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()
    verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expiration_time
    
    @property
    def expired(self):
        return self.is_expired()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_time = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('user otp')
        verbose_name_plural = _('users Otps')
    
    def __str__(self):
        return f"OTP for {self.email}"


