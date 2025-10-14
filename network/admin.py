from django.contrib import admin
from .models import Post, User, Graduate

# Register your models here.
admin.site.register(Post)
admin.site.register(Graduate)
admin.site.register(User)
