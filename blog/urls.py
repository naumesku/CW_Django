from django.urls import path, include
from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, toggle_published

app_name = BlogConfig.name

urlpatterns = [
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('published/<int:pk>', toggle_published, name='toggle_published'),
]
