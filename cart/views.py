from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import CartItem

# Create your views here.
from django.views.generic import TemplateView, ListView, DeleteView
from django.views import View


class CartView(ListView):
    model = CartItem
    template_name = 'cart/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(user = self.request.user).select_related('product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_price = sum(item.sub_total for item in context['cart_items'])
        context['total_price'] = total_price
        return context
    
# def view_cart(request):
#     context = {
#         'cart_items' : CartItem.objects.filter(user = request.user)
#         }
#     template_name = 'cart/cart.html'
#     return render(request, template_name, context)

from products.models import Product
from django.http import JsonResponse

class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('signin'))
        
        product_id = request.POST.get('product_id')
        this_product = Product.objects.get(id = product_id)

        item, created = CartItem.objects.get_or_create(user = request.user,
                                                      product = this_product)
        
        if not created:
            item.quantity += 1
            item.save()
        return JsonResponse({
            'message' : f'{this_product.title} added to Cart',
            'quantity' : item.quantity
        })
    




class UpdateCartView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('signin'))

        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        try:
            item = CartItem.objects.get(id=item_id, user=request.user)
        except CartItem.DoesNotExist:
            return redirect('cart')

        if action == "increase":
            item.quantity += 1
            item.save()

        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete() 

        elif action == "remove":
            item.delete()

        return redirect('cart_page')  
