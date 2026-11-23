from django.contrib.auth.decorators import login_required
from django.core import files
from django.shortcuts import get_object_or_404
from django.views.static import template_translatable
from django.shortcuts import render, HttpResponse, redirect
from .models import Post
from .forms import PostForm
#from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.



def home(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'azblog/home.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'azblog/post_detail.html', {'post':post})


@login_required
def post_create(request):

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('post_detail')

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

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'azblog/home.html', {'pk':post.pk})





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