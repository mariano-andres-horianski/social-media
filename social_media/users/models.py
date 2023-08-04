from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        Email and password are not in extra_fields because tehy will be used in this class before being saved.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.__db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' #specifies which field is used as unique user identifier
    REQUIRED_FIELDS = ['phone_number', 'birth_date']

    objects = CustomUserManager()
    
    class Meta:
        # The idea is that superusers can see every post analytics, tho this might be useless and I might delete it in the future
        permissions = [
            ("can_view_analytics", "Can view analytics"),
        ]
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return self.user_permissions.filter(codename=perm).exists()

    def has_module_perms(self, app_label):
        if self.is_superuser and app_label == 'social_media':
            return True
        return super().has_module_perms(app_label)