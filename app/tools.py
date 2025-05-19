from langchain.tools import tool

@tool
def initiate_return(order_id: str) -> str:
    """Initiate a return for the given order ID."""
    return f"Return process for order {order_id} has been started."

@tool
def list_discounts(category: str) -> str:
    """List current discounts in a product category."""
    return f"Currently, we are offering 20% off on all items in the '{category}' category."

@tool
def store_hours() -> str:
    """Get store opening and closing hours."""
    return "Our store is open from 9 AM to 9 PM, Monday to Saturday."

@tool
def cancel_order(order_id: str) -> str:
    """Cancel the given order."""
    return f"Order {order_id} has been successfully canceled."

@tool
def contact_support_info() -> str:
    """Provide contact information for customer support."""
    return "You can contact support at support@example.com or call 123-456-7890."

@tool
def refund_policy() -> str:
    """Provide information about the refund policy."""
    return "We offer a 30-day refund policy. Refunds are processed within 5-7 business days."
