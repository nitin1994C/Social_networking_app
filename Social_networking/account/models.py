from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    
    def create_superuser(self,email, password=None):
        user = self.create_user(
            email= self.normalize_email(email),
            password=password,
            
            
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin= True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=True)
    modified_date= models.DateField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True



class Friendship(models.Model):
    sender = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}'
    
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male','male'),
        ('female','female'),
        ('other','other')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    gender = models.CharField(max_length=11, choices=GENDER_CHOICES)
    phone_no = models.CharField(max_length=12)
    address_line_1= models.CharField(max_length=100, blank=True, null=True)
    address_line_2= models.CharField(max_length=100, blank=True, null=True)
    country= models.CharField(max_length=50, blank=True, null=True)
    city= models.CharField(max_length=35, blank=True, null=True)
    pincode= models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
    