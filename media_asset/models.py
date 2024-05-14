from django.db import models
from authentication.models import AnsaaUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone


class Zones(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = _('Sub zone')
        verbose_name_plural = _('Sub zones')

    def __str__(self):
        return self.name

class UserZone(models.Model):
    user = models.ForeignKey(AnsaaUser, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zones, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('User Zone')
        verbose_name_plural = _('User Zones')
        unique_together = ('user', 'zone')

    def __str__(self):
        return f"{self.user.fullname}'s Zone: {self.zone.name}"   


class Billboards(models.Model):

    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_COMPLETED, _('Completed')),
    ]

    VACANCY_VACANT = 'vacant'
    VACANCY_OCCUPIED = 'occupied'
    VACANCY_CHOICES = [
    (VACANCY_VACANT, _('Vacant')),
    (VACANCY_OCCUPIED, _('Occupied')),
    ]

    TYPE_ELECTRONIC = 'electronic'
    TYPE_STATIC = 'static'
    TYPE_CHOICES = [
        (TYPE_ELECTRONIC, _('Electronic')),
        (TYPE_STATIC, _('Static')),
    ]
    
    CATEGORY_CHOICES = (
        ('free standing signs','Free standing signs'),
        ('projecting signs','Projecting signs'),
        ('wall signs','Wall signs'),
        ('special advertisement','Special advertisement')
    )
    ZONE_CHOICES = (
        ('normal zone','Normal zone'),
        ('Restricted zone','Restricted zone')
    )
    asset_name = models.CharField(max_length=10, editable=False)
    asset_type = models.CharField(max_length=50, choices=TYPE_CHOICES, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    zone = models.CharField(max_length=50, choices=ZONE_CHOICES, blank=True)
    sub_zone = models.ForeignKey(Zones, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    vacancy = models.CharField(max_length=20, choices=VACANCY_CHOICES, default='vacant', blank=True)

    dimension = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    main_image = models.ImageField(upload_to="billboards/", blank=True)
    image_1 = models.ImageField(upload_to="billboards/", blank=True)
    image_2 = models.ImageField(upload_to="billboards/", blank=True)
    image_3 = models.ImageField(upload_to="billboards/", blank=True)
    user = models.ForeignKey(AnsaaUser, on_delete=models.CASCADE)

    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=20, default="Anambra", editable=False)
    country = models.CharField(max_length=20, default="Nigeria", editable=False)

    company = models.CharField(max_length=150, blank=True)
    phone_number = PhoneNumberField(blank=True)

    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.asset_name:  # Generate asset_name ID only if not already set
            asset_name_prefix = 'BOARD '
            asset_name_suffix = uuid.uuid4().hex[:3]
            self.asset_name = f'{asset_name_prefix}{asset_name_suffix}'.upper()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-status']
        verbose_name = _('Billboard')
        verbose_name_plural = _('Billboards')

    def __str__(self):
        return self.asset_name


    
