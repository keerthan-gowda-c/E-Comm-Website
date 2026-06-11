from django.shortcuts import render, redirect 

# Create your views here.

def homeView(request):
    template = 'mainapp/home.html'
    context = {
        'carousel_images' : CarouselImage.objects.filter(is_active = True)
    }
    return render(
        request = request,
        template_name = template,
        context = context
    )

def aboutView(request):
    template = 'mainapp/about.html'

    return render(
        request = request,
        template_name = template,
        context = {}
    )

def contactView(request):
    template = 'mainapp/contact.html'

    return render(
        request = request,
        template_name = template,
        context = {}
    )



from django.urls import reverse_lazy
from .models import CarouselImage

from django.views.generic import(
    CreateView,
    ListView, DetailView,
    UpdateView,
    DeleteView
)

class CarouselImageList(ListView):
    template_name = 'mainapp/carousel/carousel_list.html'
    model = CarouselImage
    context_object_name = 'carousel_images'

class AddCarouselImage(CreateView):
    model = CarouselImage
    template_name = 'mainapp/carousel/add_carousel.html'
    fields = '__all__'
    success_url = reverse_lazy('carousel_page')


class UpdateCarouselImage(UpdateView):
    model = CarouselImage
    template_name = 'mainapp/carousel/edit_carousel.html'
    fields = '__all__'
    success_url = reverse_lazy('carousel_page')


class DeleteCarouselImage(DeleteView):
    model = CarouselImage
    template_name = 'mainapp/carousel/del_carousel.html'
    success_url = reverse_lazy('carousel_page')
    context_object_name = 'carousel_image' 


from products.models import Product

def searchView(request):
    query = request.GET.get('q')

    if not query:
        return redirect(reverse_lazy('home_page'))
    
    products = Product.objects.filter(title__icontains = query)

    context = {
        'query' : query,
        'products' : products
    }
    template = 'mainapp/search_results.html'
    return render(request, template, context)