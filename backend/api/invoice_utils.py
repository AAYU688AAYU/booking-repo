from decimal import Decimal
from .models import Invoice, Booking


def generate_booking_invoice(booking: Booking, payment_tx=None) -> Invoice:
    """
    Creates or updates the legal tax invoice for a confirmed booking.
    Calculates subtotal, 5% standard GST/tourism tax, and net payable.
    """
    if hasattr(booking, 'invoice'):
        inv = booking.invoice
        if payment_tx and not inv.is_paid:
            inv.is_paid = True
            inv.save()
        return inv

    total = booking.total_price
    # Assume price is gross; tax is 5%
    tax_rate = Decimal('5.00')
    subtotal = (total / (Decimal('1.00') + (tax_rate / Decimal('100.00')))).quantize(Decimal('0.01'))
    tax_amount = (total - subtotal).quantize(Decimal('0.01'))

    invoice = Invoice.objects.create(
        booking=booking,
        billing_name=booking.customer_name,
        billing_email=booking.customer_email,
        subtotal=subtotal,
        tax_rate_percent=tax_rate,
        tax_amount=tax_amount,
        total_amount=total,
        currency='USD',
        is_paid=(booking.status == 'CONFIRMED'),
        pdf_url=f"/api/bookings/{booking.booking_reference}/invoice/download/"
    )
    return invoice
