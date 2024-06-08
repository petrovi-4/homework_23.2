from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from pytils.translit import slugify

from blog.models import BlogPost


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'content', 'preview_image', 'is_published')
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        base_slug = slugify(form.instance.title)
        unique_slug = base_slug
        while BlogPost.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{base_slug}-{get_random_string(4)}'
        form.instance.slug = unique_slug
        form.instance.save()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ('title', 'content', 'preview_image', 'is_published')

    def get_success_url(self):
        return reverse('blog:view', args=[self.object.slug])


class BlogPostListView(ListView):
    model = BlogPost
    extra_context = {
        'title': 'Блог'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogPostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(slug=self.kwargs.get('slug'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        blogpost_item = BlogPost.objects.get(slug=self.kwargs.get('slug'))
        context_data['slug'] = blogpost_item.slug
        context_data['title'] = blogpost_item.title
        return context_data


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:list')
