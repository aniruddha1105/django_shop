# shopping_cart/urls.py
from django.urls import path
from .views import product_list, add_to_cart,  home_view
from .views import view_cart, update_cart
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [



    path('', product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    path('home/', home_view, name='home'),


    path('view-cart/', view_cart, name='view_cart'),
    path('update-cart/', update_cart, name='update_cart'),






]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
