from django.db import models 
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin 
from .managers import UserManager 
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractBaseUser,PermissionsMixin):

    ROLE_CHOICES=(
       ( 'student','Student'),
       ('faculty','Faculty'),
       ('alumni','Alumni'),
    )

    email=models.EmailField(unique=True)
    username=models.CharField(max_length=100)
    role=models.CharField(max_length=10,choices=ROLE_CHOICES)

    college=models.CharField(max_length=150)
    department=models.CharField(max_length=100)

    phone=models.CharField(max_length=15,blank=True)
    location=models.CharField(max_length=100,blank=True)

    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    date_joined=models.DateTimeField(default=timezone.now)

    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    headline=models.CharField( max_length=150,blank=True)
    bio=models.TextField(blank=True,help_text="Tell us About Yourself.")

    year=models.CharField(max_length=20,blank=True,null=True,default="First Year",help_text="Year of graduation.")

    profile_pic=models.ImageField(upload_to='profiles/',default='default.png',help_text="Upload Your Profile Picture.")
    cover_pic=models.ImageField(upload_to='covers/',blank=True,help_text="Upload Your Cover Picture.")
    skills=models.CharField(max_length=255,blank=True,help_text="Comma seperated skills")
    connections = models.ManyToManyField("self", blank=True)

    github=models.URLField(blank=True)
    linkdin=models.URLField(blank=True)
    portfolio=models.URLField(blank=True)

    resume=models.FileField(upload_to='resumes/',blank=True)

    followers=models.ManyToManyField(User,related_name="Followers",blank=True)

    is_verified=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}Profile"
    


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()