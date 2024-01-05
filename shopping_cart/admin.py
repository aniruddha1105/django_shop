# shopping_cart/admin.py
from django.contrib import admin
from .models import Product, Cart, CartItem, Category


class CartItemInline(admin.TabularInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'display_image')
    list_filter = ('category',)

    def display_image(self, obj):
        return obj.image.url if obj.image else ''


admin.site.register(Product, ProductAdmin)


admin.site.register(Cart, CartAdmin)
