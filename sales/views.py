from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderedItem, Order
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import DetailView, View
from django.utils import timezone


def products(request):
    context = {
        'items': Item.objects.all()
    }

    return render(request, "product-page.html", context)



class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'

@login_required
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
            messages.info(request, "The item qty was updated successfully ")

        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            #return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to the cart successfully")
    
    return redirect("products",slug= slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderedItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("products", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("products", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item =  OrderedItem.objects.filter(
            item=item,
            user = request.user,
            ordered = False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
            return redirect("home-page")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("products", slug=slug)
    else:
        messages.info(request, "Aint nobody got time for that, try again")
        return redirect("products", slug = slug )

class HomeView(ListView):

    model= Item
    paginate_by = 1
    template_name = 'home-page.html'
   
class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")




        

    
    

    







def check_out(request):

    return render(request, 'checkout-page.html')