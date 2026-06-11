from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Product
from . import forms

from django.views.generic import(
    CreateView,
    ListView, DetailView,
    UpdateView,
    DeleteView
)

from django.urls import reverse_lazy, reverse


# class ProductList(ListView):
#     template_name = 'products/product_list'
#     model = Product
#     context_object_name = 'products'

from django.views.generic.edit import FormMixin

class ProductDetailView(FormMixin,DetailView):
    template_name = 'products/product_details.html'
    model = Product
    context_object_name = 'product'
    form_class = forms.ProductImageForm


    def get_success_url(self):
        return reverse('product_details', kwargs = {'pk' : self.this_product.pk})

    def post(self, request, *args, **kwargs):
        self.this_product = self.get_object()
        submitted_image_form = self.get_form()

        if submitted_image_form.is_valid():
            product_image = submitted_image_form.save(commit = False)
            product_image.product = self.this_product
            product_image.save()
            return redirect(self.get_success_url())
            

class AddProduct(CreateView):
    model = Product
    template_name = 'products/add_product.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')


class UpdateProduct(UpdateView):
    model = Product
    template_name = 'products/edit_product.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')


class DeleteProduct(DeleteView):
    model = Product
    template_name = 'products/del_product.html'
    success_url = reverse_lazy('product_list')
    context_object_name = 'product' 


from .models import ProductImage



class AddProductImageView(CreateView):
    model = ProductImage
    form_class = forms.ProductImageForm
    success_url = reverse_lazy('product_details')
    
    template_name = 'products/add_product_image.html'

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.product = self.product
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk': self.product.pk}) # OR redirect manually

class UpdateProductImage(UpdateView):
    model = ProductImage
    template_name = 'products/edit_product_image.html'
    form_class = forms.ProductImageForm
    success_url = reverse_lazy('product_list')


class DeleteProductImage(DeleteView):
    model = ProductImage
    template_name = 'products/del_product_image.html'
    success_url = reverse_lazy('product_list')
    context_object_name = 'product_image' 


from .models import Category
from .forms import CategoryForm

class CategoryList(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'


class AddCategory(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/add_category.html'
    success_url = reverse_lazy('category_list')


class UpdateCategory(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/edit_category.html'
    success_url = reverse_lazy('category_list')

class DeleteCategory(DeleteView):
    model = Category
    template_name = 'category/del_category.html'
    success_url = reverse_lazy('category_list')
    context_object_name = 'category'


class ProductList(ListView):
    template_name = 'products/product_list.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        category_pk = self.kwargs.get('pk')

        if category_pk:
            return Product.objects.filter(category_id=category_pk)

        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context