"""sales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
#from .views import views

from .views import HomeView
from .views import  ItemDetailView, add_to_cart, remove_from_cart #OrderSummaryView
from .  import views

app_name = 'sales'

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    #path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('products/<slug>', ItemDetailView.as_view(),  name="products"),
    path('checkout/', views.check_out),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart")
]
