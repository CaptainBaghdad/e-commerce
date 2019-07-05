from django.shortcuts import render
from .models import Item
from django.views.generic import ListView
from django.views.generic import DetailView


def products(request):
    context = {
        'items': Item.objects.all()
    }

    return render(request, "product-page.html", context)



class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'

class HomeView(ListView):

    model= Item
    template_name = 'home-page.html'

    







def check_out(request):

    return render(request, 'checkout-page.html')