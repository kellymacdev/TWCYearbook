from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

class Post(models.Model):
    content = models.TextField()
    likes = models.ManyToManyField(User, symmetrical=False, null=True, blank=True, related_name='liked_posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id}"

    def serialize(self, user=None):
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user.username,
            "likes": self.likes.count(),
            "liked": user.is_authenticated and self.likes.filter(id=user.id).exists() if user else False,
            "my_post": user.is_authenticated and self.user == user if user else False,
        }

class Graduate(models.Model):
    name = models.TextField()
    maiden_name = models.TextField(blank=True, null=True)
    pronouns = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    industry = models.TextField(blank=True, null=True)
    gen_description = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    q1 = models.TextField(blank=True, null=True)
    q2 = models.TextField(blank=True, null=True)
    q3 = models.TextField(blank=True, null=True)
    q4 = models.TextField(blank=True, null=True)
    q5 = models.TextField(blank=True, null=True)
    q6 = models.TextField(blank=True, null=True)
    q7 = models.TextField(blank=True, null=True)
    q8 = models.TextField(blank=True, null=True)
    q9 = models.TextField(blank=True, null=True)
    q10 = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)
    school_years = models.IntegerField(blank=True, null=True)
    countries = models.IntegerField(blank=True, null=True)
    jobs = models.IntegerField(blank=True, null=True)
    tattoos = models.IntegerField(blank=True, null=True)
    married = models.BooleanField(default=False)
    babies = models.IntegerField(blank=True, null=True)
    for_zaza = models.TextField(blank=True, null=True)
    for_linda = models.TextField(blank=True, null=True)
    spotify = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

