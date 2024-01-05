# shopping_cart/views.py

from .models import Cart, CartItem, Product

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.views.decorators.http import require_POST

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.contrib import messages

from .forms import UpdateCartForm

from django.contrib import messages


def home_view(request):
    products = Product.objects.all()
    return render(request, 'shopping_cart/product_list.html', {'products': products})


def home(request):
    # Fetch some featured products for the carousel
    featured_products = Product.objects.filter(featured=True)[:3]

    context = {
        'featured_products': featured_products,
    }

    return render(request, 'shopping_cart/home.html', context)


# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'shopping_cart/product_list.html', {'products': products})
def product_list(request):
    search_query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=search_query)

    context = {
        'products': products,
    }
    return render(request, 'shopping_cart/product_list.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('product_list')


def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price *
                      item.quantity for item in cart_items)

    return render(request, 'shopping_cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


@require_POST
# shopping_cart/views.py
# ... (rest of the code remains the same)
def update_cart(request):
    if request.method == 'POST':
        form = UpdateCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            action = form.cleaned_data['action']

            cart = Cart.objects.get(user=request.user)

            try:
                cart_item = CartItem.objects.get(
                    cart=cart, product__id=product_id)
                if action == 'update':
                    quantity = form.cleaned_data['quantity']
                    cart_item.quantity = quantity
                    cart_item.save()
                    messages.success(request, 'Cart updated successfully.')
                elif action == 'remove':
                    cart_item.delete()
                    messages.warning(request, 'Product removed from the cart.')
            except CartItem.DoesNotExist:
                # Handle the case where the item is not found in the cart
                pass

            return redirect('view_cart')

    # Handle the case where the form is not valid or the request method is not POST
    # You might want to redirect to a different page
    return redirect('view_cart')

# Add other views as needed


def update_cart(request):
    if request.method == 'POST':
        form = UpdateCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            action = form.cleaned_data['action']

            cart = Cart.objects.get(user=request.user)

            try:
                cart_item = CartItem.objects.get(
                    cart=cart, product__id=product_id)
                if action == 'update':
                    quantity = form.cleaned_data['quantity']
                    cart_item.quantity = quantity
                    cart_item.save()
                    messages.success(request, 'Cart updated successfully.')
                elif action == 'remove':
                    cart_item.delete()
                    messages.warning(request, 'Product removed from the cart.')
            except CartItem.DoesNotExist:
                pass

            return redirect('view_cart')

    return redirect('view_cart')
