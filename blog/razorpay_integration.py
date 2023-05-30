import razorpay
from django.conf import settings

def create_razorpay_order(amount, currency='INR'):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    data = {
        'amount': amount * 100,  # Razorpay expects the amount in paise
        'currency': currency,
        'payment_capture': '1'
    }
    order = client.order.create(data=data)
    return order['id']
