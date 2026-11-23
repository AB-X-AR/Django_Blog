from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')