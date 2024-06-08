from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import never_cache

from blog.apps import BlogConfig
from blog.views import BlogPostListView, BlogPostCreateView, BlogPostDetailView, BlogPostUpdateView, BlogPostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    path('create/', never_cache(BlogPostCreateView.as_view()), name='create'),
    path('edit/<slug>', never_cache(BlogPostUpdateView.as_view()), name='edit'),
    path('view/<slug>', BlogPostDetailView.as_view(), name='view'),
    path('delete/<slug>', BlogPostDeleteView.as_view(), name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
