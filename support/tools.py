from orders.models import Product, Order, RefundRequest
from django.utils import timezone
from .tracking_data import DELIVERY_DATA


def get_order_details(order_id):
    try:
        order = Order.objects.get(id=order_id)
        return {
            'id': order.id,
            'user': order.user.username,
            'product_name': order.product_name,
            'amount': str(order.amount),
            'status': order.get_status_display(),
            'carrier': order.carrier,
            'tracking_number': order.tracking_number,
            'delivery': order.delivery,
            'ordered_on': order.created_at.strftime("%d %b%Y"),
            'days_since_order': (timezone.now() - order.created_at).days
        }
    except Order.DoesNotExist:
        return {"error": f"Order #{id} not found."}
    

def get_refund_history(user_id):
    refunds = RefundRequest.objects.filter(user_id=user_id).order_by("-created_at")
    
    history = []
    for refund in refunds:
        history.append({
            "order_id" : refund.order.id,
            "product": refund.order.product_name,
            "reason": refund.reason,
            "status": refund.status,
            "requested_on": refund.created_at.strftime("%d %b %Y"),
        })
    return {
        "total_refund_requests" : len(history),
        "history": history
    }


def check_delivery_status(tracking_number, carrier):
    default_response = {
        "status": "Unknown",
        "last_location": "Tracking information not available",
        "last_update": "N/A",
        "estimated_delivery": "Contact carrier directly",
        "delay_reason": "No update from carrier",
    }

    result = DELIVERY_DATA.get(tracking_number, default_response)
    result["tracking_number"] = tracking_number
    result["carrier"] = carrier
    return result

