from django.shortcuts import render, get_object_or_404, redirect

# Authentications
from django.contrib.auth.decorators import login_required

# Model
from App_Order.models import Cart, Order
from App_Shop.models import Product
# Messages
from django.contrib import messages


# Create your views here.

@login_required
def add_to_cart(request, pk):
    # Retrieving the item
    item = get_object_or_404(Product, pk=pk)
    print("Item")
    print(item)
    # Running the query if item is in cart
    order_item_qs = Cart.objects.get_or_create(
        item=item, user=request.user, purchased=False)
    # Retrieving the item from query
    order_item = order_item_qs[0]
    print("Order Item Object:")
    print(order_item_qs)
    print(order_item_qs[0])
    # Running a query if there is an order that was created
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print("Order Qs:")
    print(order_qs)
    # Checking if there is a order that exists or doesnt
    if order_qs.exists():
        # Retrieving the order from query bcz it exists
        order = order_qs[0]
        print(order_qs[0])
        print("If Order exist")
        print(order)
        # Checking if the item is in already in orderList or not
        if order.orderitems.filter(item=item).exists():
            # Incresing item's quantity bcz its already in orderList and save it.
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("App_Shop:product_detail", pk=item.pk)
        else:
            # Adding the item in orderList bcz it doesnt exist yet
            order.orderitems.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("App_Shop:product_detail", pk=item.pk)
    else:
        # There is no ORDER! so CREATE and SAVE IT!
        order = Order(user=request.user)
        order.save()
        # And then add the item in orderList
        order.orderitems.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("App_Shop:product_detail", pk=item.pk)


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    isExists = False
    if carts.exists() and orders.exists():
        # Retrieving the order from query
        order = orders[0]
        isExists = True
        return render(request, 'App_Order/cart.html', context={'carts': carts, 'order': order, 'isExists': isExists})
    else:
        return render(request, 'App_Order/cart.html', context={'isExists': isExists})


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed form your cart")
            return redirect("App_Order:cart")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")


@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(
                    request, f"{item.name}'s quantity has been updated")
                return redirect("App_Order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")


@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(
                    request, f"{item.name}'s quantity has been updated")
                return redirect("App_Order:cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(
                    request, f"{item.name} item has been removed from your cart")
                return redirect("App_Order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")
