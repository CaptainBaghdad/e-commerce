from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderedItem, Order
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic import DetailView
from django.utils import timezone


def products(request):
    context = {
        'items': Item.objects.all()
    }

    return render(request, "product-page.html", context)



class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'

def add_to_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderedItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False
        
        )
    
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug= item.slug).exists():
            order_item.quantity += 1
            order_item.save()

        else:
            order.items.add(order_item)
            #messages.info(request, "This item was added to your cart.")
            #return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    
    return redirect("products",slug= slug)

class HomeView(ListView):

    model= Item
    template_name = 'home-page.html'

    







def check_out(request):

    return render(request, 'checkout-page.html')