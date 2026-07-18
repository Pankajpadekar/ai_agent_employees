from django.shortcuts import get_object_or_404, render
from .models import Order, RefundRequest
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)  # Filter orders based on the logged-in user
    context = {'orders': orders}
    return render(request, 'orders_list.html', context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)  # Ensure the order belongs to the logged-in user

    #get refund history for the order
    refunds = RefundRequest.objects.filter(order=order, user=request.user)
    context = {'order': order, 'refunds': refunds}
    return render(request, 'order_detail.html', context)