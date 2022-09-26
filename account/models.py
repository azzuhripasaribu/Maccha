from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user( self, email, username, full_name, company_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Please input your email address !")
        if not username:
            raise ValueError("Please input your username !")
        if not full_name:
            raise ValueError("Please input your full name !")
        if not company_name:
            raise ValueError("Please input your full name !")
        if not password:
            raise ValueError("Please input your password !")
        
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            username=username,
            company_name=company_name,
        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, full_name, password=None):
        user = self.create_user(
            email,
            username=username,
            full_name=full_name,
            password=password,
            is_staff=True
        )
        return user
    
    def create_superuser(self, email, username, full_name, password=None):
        user = self.create_user(
            email,
            username=username,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','full_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_active(self):
        return self.active
    
    @property
    def is_admin(self):
        return self.admin