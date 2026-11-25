from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.core.exceptions import PermissionDenied
#from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'azblog/login.html') 

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('home')

def home(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'azblog/home.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Prevent IDOR: unauthenticated or unauthorized users cannot view unpublished drafts
    if post.status != 'published':
        if not request.user.is_authenticated or (post.author != request.user and not request.user.is_staff):
            raise Http404("Post not found.")
    return render(request, 'azblog/post_detail.html', {'post':post})


@login_required
def post_create(request):

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()

    return render(request, 'azblog/post_form.html', {'form': form})
        
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, "azblog/post_form.html", {'form':form, 'pk':post.pk})
        
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            post.delete()
            messages.success(request, 'Post Deleted Successfully')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password. Post was not deleted')
    return render(request, 'azblog/post_confirm_delete.html', {'post':post})





"""

#READ ALL
class HomeView(ListView):
    model = Post
    template_name = 'azblog/home.html'

#READ SINGLE
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'azblog/article_details.html'

#CREATE
class ArticleCreate(CreateView):
    model = Post
    template_name = 'azblog/post_form.html'
    fields = ['title', 'excerpt', 'content', 'status']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#UPDATE
class ArticleUpdate(UpdateView):
    model = Post
    template_name = 'azblog/post_form.html'
    fields = ['title', 'excerpt', 'content', 'status']
    def test_func(self):
        return self.request.user == self.get_object().author
"""