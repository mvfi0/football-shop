from django import template
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

register = template.Library()

@register.filter(name="rupiah")
def rupiah(value, show_symbol=True):
    """
    Format a number as Indonesian Rupiah.
    Usage:
      {{ value|rupiah }}               -> "Rp 5.000.000"
      {{ value|rupiah:False }}         -> "5.000.000" (no Rp)
    """
    try:
        value = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value

    value = value.quantize(Decimal("1."), rounding=ROUND_HALF_UP)
    formatted = f"{value:,.0f}".replace(",", ".")
    return f"Rp {formatted}" if str(show_symbol).lower() != "false" else formatted
