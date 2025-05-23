from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from typing import Optional, List, Dict, Any

from app.tools import ALL_TOOLS, get_tool_descriptions
from app.prompts import create_agent_prompt, get_concise_prompt, get_detailed_prompt
from config import settings

app = FastAPI(
    title="Customer Service Chatbot API",
    description="AI-powered customer service assistant with tool integration",
    version="1.0.0",
)


class Query(BaseModel):
    question: str
    response_style: Optional[str] = "default"  # "default", "concise", "detailed"


class ChatResponse(BaseModel):
    response: str
    intermediate_steps: Optional[List[Dict[str, Any]]] = None
    tools_used: Optional[List[str]] = None


class HealthResponse(BaseModel):
    status: str
    message: str


class CapabilitiesResponse(BaseModel):
    available_tools: Dict[str, str]
    response_styles: List[str]


def create_llm():
    """Create and configure the language model."""
    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")

    return ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=settings.TEMPERATURE,
    )


def create_agent_executor(response_style: str = "default"):
    """Create agent executor with specified response style."""
    llm = create_llm()

    # Select prompt based on style
    if response_style == "concise":
        prompt = get_concise_prompt()
    elif response_style == "detailed":
        prompt = get_detailed_prompt()
    else:
        prompt = create_agent_prompt()

    # Create agent
    agent = create_tool_calling_agent(llm, ALL_TOOLS, prompt)

    # Create executor
    return AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=settings.VERBOSE,
        max_iterations=settings.MAX_ITERATIONS,
        return_intermediate_steps=True,
    )


# Global agent executor (you might want to implement caching/pooling for production)
agent_executors = {}


def get_agent_executor(style: str = "default"):
    """Get or create agent executor for the specified style."""
    if style not in agent_executors:
        agent_executors[style] = create_agent_executor(style)
    return agent_executors[style]


# API Routes
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint returning API information."""
    return HealthResponse(
        status="running", message="Customer Service Chat API is operational"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Test LLM connection
        llm = create_llm()
        return HealthResponse(status="healthy", message="All systems operational")
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(err)}")


@app.get("/capabilities", response_model=CapabilitiesResponse)
async def get_capabilities():
    """Get available tools and response styles."""
    return CapabilitiesResponse(
        available_tools=get_tool_descriptions(),
        response_styles=["default", "concise", "detailed"],
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(query: Query):
    """Main chat endpoint for customer service interactions."""
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Get appropriate agent executor
        agent_executor = get_agent_executor(query.response_style)

        # Execute the query
        result = await agent_executor.ainvoke({"input": query.question})

        # Extract tools used from intermediate steps
        tools_used = []
        if result.get("intermediate_steps"):
            for step in result["intermediate_steps"]:
                if hasattr(step[0], "tool") and step[0].tool:
                    tools_used.append(step[0].tool)

        return ChatResponse(
            response=result["output"],
            intermediate_steps=(
                result.get("intermediate_steps", []) if settings.VERBOSE else None
            ),
            tools_used=list(set(tools_used)) if tools_used else None,
        )

    except Exception as err:
        # Log the error (implement proper logging in production)
        print(f"Error processing chat request: {str(err)}")

        return ChatResponse(
            response="I apologize, but I encountered an error while processing your request. "
            "Please contact support at support@example.com or call 123-456-7890 for immediate assistance.",
            intermediate_steps=None,
            tools_used=None,
        )


@app.post("/chat/concise", response_model=ChatResponse)
async def chat_concise(query: Query):
    """Chat endpoint optimized for brief responses."""
    query.response_style = "concise"
    return await chat(query)


@app.post("/chat/detailed", response_model=ChatResponse)
async def chat_detailed(query: Query):
    """Chat endpoint optimized for comprehensive responses."""
    query.response_style = "detailed"
    return await chat(query)


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle configuration errors."""
    return HTTPException(status_code=500, detail=f"Configuration error: {str(exc)}")


if __name__ == "__main__":
    import uvicorn

    try:
        create_llm()
        print("Configuration validated successfully")
    except Exception as e:
        print(f"Configuration error: {e}")
        exit(1)

    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "false").lower() == "true",
    )
