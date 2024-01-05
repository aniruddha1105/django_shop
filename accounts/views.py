# account/views.py
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from .models import Account
from shopping_cart.models import Cart, CartItem
from django.contrib.auth import logout
from shopping_cart.forms import UpdateCartForm


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        # Custom logic if needed before logging in
        response = super().form_valid(form)
        # Redirect the user to the home page after successful login
        return redirect('home')


def logout_view(request):
    # Custom logout logic, if needed
    logout(request)
    # Redirect to a specific page after logout (e.g., home page)
    return redirect('login')


@login_required
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


# accounts/views.py


def register_view(request):
    template_name = 'registration.html'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to the home page after successful registration
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})
