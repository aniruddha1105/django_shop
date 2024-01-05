from django.urls import path
from .views import CustomLoginView, register_view,logout_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='registration'),
      path('logout/', logout_view, name='logout'),
    # Add other URLs as needed
]
