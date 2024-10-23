from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Coffee, Cart, CartItem


def home(request):
    if "q" in request.GET:
        q = request.GET["q"]
        multiple_q = Q(Q(name__icontains=q) | Q(price__icontains=q))
        coffee = Coffee.objects.filter(multiple_q)
    else:
        coffee = Coffee.objects.all()
    return render(request, "home.html", {"coffee": coffee})


@login_required
def add_to_cart(request, coffee_id):
    """Adds a coffee to the user's cart or updates the quantity if already present."""
    coffee = get_object_or_404(Coffee, pk=coffee_id)
    user = request.user

    try:
        cart_item = CartItem.objects.get(cart__user=user, product=coffee)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Updated {coffee.name} quantity in your cart.")
    except CartItem.DoesNotExist:
        cart, created = Cart.objects.get_or_create(user=user, active=True)
        cart_item = CartItem.objects.create(cart=cart, product=coffee, quantity=1)
        messages.success(request, f"Added {coffee.name} to your cart.")

    request.session["cart_count"] = CartItem.objects.filter(cart__user=user).count()
    return redirect("cart_detail")


@login_required
def cart_detail(request):
    """Displays the contents of the user's cart."""
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    total = sum(item.quantity * item.product.price for item in cart_items)

    context = {"cart_items": cart_items, "total": total}
    return render(request, "cart_detail.html", context)
