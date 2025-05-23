"""
Customer service tools for the retail store chatbot.
"""

from langchain.tools import tool


@tool
def initiate_return(order_id: str) -> str:
    """Initiate a return for the given order ID."""
    return f"Return process for order {order_id} has been started. You will receive a return label via email within 24 hours."


@tool
def list_discounts(category: str = "all") -> str:
    """List current discounts in a product category. If no category specified, shows all discounts."""
    discounts = {
        "electronics": "25% off all electronics",
        "clothing": "30% off summer collection",
        "books": "Buy 2 get 1 free",
        "home": "20% off home decor items",
    }

    if category.lower() == "all":
        return "Current discounts: " + ", ".join(discounts.values())
    elif category.lower() in discounts:
        return f"Current discount for {category}: {discounts[category.lower()]}"
    else:
        return f"No current discounts available for '{category}' category."


@tool
def store_hours() -> str:
    """Get store opening and closing hours."""
    return "Our store hours are: Monday-Saturday 9 AM to 9 PM, Sunday 10 AM to 8 PM. Holiday hours may vary."


@tool
def cancel_order(order_id: str) -> str:
    """Cancel the given order."""
    return f"Order {order_id} has been successfully canceled. Refund will be processed within 3-5 business days if payment was already made."


@tool
def contact_support_info() -> str:
    """Provide contact information for customer support."""
    return """Customer Support Information:
    📧 Email: support@example.com
    📞 Phone: 123-456-7890
    💬 Live Chat: Available on our website 24/7
    📍 Address: 123 Main St, City, State 12345
    Hours: Monday-Friday 8 AM to 8 PM"""


@tool
def refund_policy() -> str:
    """Provide information about the refund policy."""
    return """Refund Policy:
    • 30-day return window from purchase date
    • Items must be in original condition with tags
    • Refunds processed within 5-7 business days
    • Original shipping costs are non-refundable
    • Digital products are non-refundable after download"""


ALL_TOOLS = [
    initiate_return,
    list_discounts,
    store_hours,
    cancel_order,
    contact_support_info,
    refund_policy,
]


def get_tool_descriptions():
    """Return a dictionary of tool names and their descriptions for API documentation."""
    return {
        "initiate_return": "Start a return process for an order",
        "list_discounts": "Get current discounts and promotions",
        "store_hours": "Get store operating hours",
        "cancel_order": "Cancel an existing order",
        "contact_support_info": "Get customer support contact information",
        "refund_policy": "Get detailed refund policy information",
    }
