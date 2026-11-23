from django.urls import path
#from .views import HomeView, ArticleDetailView
from . import views
# d , D


urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.home, name="home"),
    path('post/<int:pk>', views.post_detail, name="post_detail"),
    path('post/create/', views.post_create, name='post_create'),
    path('post/edit/<int:pk>', views.post_update, name="post_update"),
    path('post/delete/<int:pk>', views.post_delete, name='post_delete'),
    #path('article/<int:pk>', ArticleDetailView.as_view(), name="article-details")
]

