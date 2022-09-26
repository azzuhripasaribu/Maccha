from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save


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
    
class Profile(models.Model):
    user   = models.OneToOneField(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default_profile.png')

    def __str__(self) -> str:
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        profile_image = Image.open(self.image.path)
        if profile_image.height > 200 or profile_image.width > 200:
            rescale_profile_image = (200,200)
            profile_image.thumbnail(rescale_profile_image)
            profile_image.save(self.image.path)

@receiver(post_save, sender=Account)
def create_profile_account(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#@receiver(post_save, sender=Account)
#def save_user_profile(sender, instance, **kwargs):
    #instance.profile.save()
