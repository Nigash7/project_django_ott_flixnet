
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager): 
    def create_user(self, email, name=None, password=None, **extra_fields): 
        if not email: 
            raise ValueError("Users must have an email address") 
        email = self.normalize_email(email) 
        user = self.model(email=email, name=name, **extra_fields) 
        user.set_password(password) 
        user.save(using=self._db) 
        return user 
                
    def create_superuser(self, email, password=None, **extra_fields): 
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):  # ✅ Added PermissionsMixin
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)     # ✅ Required for admin login
    is_superuser = models.BooleanField(default=False) # ✅ Required for permissions

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    

    def __str__(self):
        return self.title
class movie(models.Model):
    video_file = models.FileField(upload_to='videos/', )
    thumbnail = models.ImageField(upload_to='imgs/',)
    title = models.CharField(max_length=100)
    description = models.TextField()  

class watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(movie, on_delete=models.CASCADE) 
    date = models.DateTimeField(auto_now_add=True)
class history_view(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(movie, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

# Create your models here.
