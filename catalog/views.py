from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, CreateView, ListView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version
from catalog.services import get_categories_from_cache


class IndexView(TemplateView):
    template_name = 'catalog/catalog_list.html'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.all().order_by('-id')[:5]
        return context_data


class ContactView(TemplateView):
    template_name = 'catalog/contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'Новое сообщение от пользователя {name}({email}): {message}')
        return self.render_to_response({'title': 'Контакты'})


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_item = Product.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = product_item.product_name
        if product_item.version_set.filter(is_active=True):
            context_data['version'] = product_item.version_set.filter(is_active=True).last()
        else:
            context_data['version'] = None
        return context_data


@permission_required('catalog.can_canceled_publication')
def toggle_publish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = not product.is_published
    product.save()
    return redirect(reverse('catalog:product', args=[pk]))


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list_product')

    def form_valid(self, form):
        new_product = form.save()
        new_product.owner = self.request.user
        new_product.save()
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Список товаров'
    }


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list_product')

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        if user == product.owner:
            return True

        required_perms = [
            'catalog.can_edit_description',
            'catalog.can_edit_category',
            'catalog.can_canceled_publication'
        ]

        return all(user.has_perm(perm) for perm in required_perms)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm

        required_perms = [
            'catalog.can_edit_description',
            'catalog.can_edit_category',
            'catalog.can_canceled_publication'
        ]

        if all(user.has_perm(perm) for perm in required_perms):
            return ProductModeratorForm

        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list_product')

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user or self.request.user.has_perm('catalog.delete_product')


class VersionCreateView(LoginRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/version_form.html'  # добавлено
    success_url = reverse_lazy('catalog:list_product')


class VersionDetailView(DetailView):
    model = Version


class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:list_product')


class VersionDeleteView(LoginRequiredMixin, DeleteView):
    model = Version
    success_url = reverse_lazy('catalog:list_product')


def categories(request):
    context = {
        'object_list': get_categories_from_cache(),
        'title': 'Категории'
    }
    return render(request, 'catalog/categories.html', context)
