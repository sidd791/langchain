"""
Prompt templates for the customer service chatbot.
"""

from langchain_core.prompts import ChatPromptTemplate

# System prompt for the customer service agent
SYSTEM_PROMPT = """You are a helpful customer service assistant for an online retail store. 
You have access to various tools to help customers with their inquiries.

Guidelines:
- Be friendly, professional, and helpful
- Use the appropriate tools to provide accurate information
- If you need specific information like order IDs, ask the customer to provide them
- Always try to resolve the customer's issue completely
- If you cannot help with something, direct them to contact support
- Keep responses concise but informative
- Always confirm important actions (like cancellations or returns) with the customer

Available tools:
- initiate_return: Start a return process for an order
- list_discounts: Get current discounts and promotions
- store_hours: Get store operating hours
- cancel_order: Cancel an existing order
- contact_support_info: Get customer support contact information
- refund_policy: Get detailed refund policy information
"""


def create_agent_prompt():
    """Create and return the chat prompt template for the agent."""
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )


def create_custom_prompt(system_message: str = None):
    """Create a custom prompt template with optional system message override."""
    if system_message is None:
        system_message = SYSTEM_PROMPT

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )


# Alternative prompts for different use cases
CONCISE_SYSTEM_PROMPT = """You are a quick-response customer service bot. 
Provide brief, direct answers using available tools. 
Be helpful but keep responses short and to the point."""

DETAILED_SYSTEM_PROMPT = """You are a comprehensive customer service assistant.
Provide detailed explanations and thoroughly address customer concerns.
Use multiple tools if necessary to fully resolve issues.
Ask follow-up questions to ensure complete customer satisfaction."""


def get_concise_prompt():
    """Return a prompt template optimized for brief responses."""
    return create_custom_prompt(CONCISE_SYSTEM_PROMPT)


def get_detailed_prompt():
    """Return a prompt template optimized for comprehensive responses."""
    return create_custom_prompt(DETAILED_SYSTEM_PROMPT)
