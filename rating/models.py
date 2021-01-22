from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phone_field import PhoneField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    bio = models.TextField(max_length=500, blank=True, default='No bio')
    profile_pic = models.ImageField(upload_to='profile/', default='a.png')

    @classmethod
    def search_by_profile(cls, username):
        certain_user = cls.objects.filter(user__username__icontains = username)
        return certain_user

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
         if created:
            Profile.objects.create(user=instance)
            instance.profile.save()   

    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile       

class Project(models.Model):
    title = models.CharField(max_length=250, blank=True)
    project_pic = models.ImageField(upload_to='projectpic/')
    description = models.TextField(max_length=255)
    project_link = models.URLField(max_length = 200) 
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')

    class Meta:
        ordering = ["-pk"]

    def save_project(self):
        self.save()

    def get_absolute_url(self):
        return f"/project/{self.id}"


    def delete_project(self):
        self.delete()

    def __str__(self):
        return self.title


class Rate(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rate')
    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating,default=0, blank=True)
    content = models.IntegerField(choices=rating,default=0, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def save_rate(self):
        self.save()

    class Meta:
        ordering = ["-pk"]                 