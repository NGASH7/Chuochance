from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from applications.models import Period, Application

from .manager import UserManager
# Create your models here.
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

USER_TYPE_CHOICES = (
    (0, 'Superuser'),
    (1, 'Staff'),
    (2, 'Applicant')
)


class User(AbstractUser):
    user_type = models.PositiveSmallIntegerField(
        null=True, choices=USER_TYPE_CHOICES)
    user_type_desc = models.CharField(max_length=40, null=True)
    other_names = models.CharField(null=True, blank=True, max_length=150)

    id_number = models.CharField(
        null=True, blank=True, max_length=10, unique=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, null=True,
                              blank=True, choices=GENDER)
    phone = models.CharField(max_length=13, null=True, blank=True)
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'id_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.id_number}'

    # def save(self, *args, **kwargs):
    #     self.username = self.id_number
    #     super(User, self).save(*args, **kwargs)

    @property
    def applications(self):
        """
        docstring
        """
        return self.applications.all()

    @property
    def current_application(self):
        """
        docstring
        """
        return self.applications.get(period=Period.objects.get(year=datetime.today().year))
