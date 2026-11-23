from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta: #For Which model the form is Created
        model = Post
        fields = ['title', 'slug', 'content', 'excerpt', 'status']


