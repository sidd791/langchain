from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from app.tools import (
    initiate_return,
    list_discounts,
    store_hours,
    cancel_order,
    contact_support_info,
    refund_policy
)

app = FastAPI()

llm = OllamaLLM(model="llama3")

tool_list = [
    initiate_return,
    list_discounts,
    store_hours,
    cancel_order,
    contact_support_info,
    refund_policy,
]

agent = initialize_agent(
    tools=tool_list,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

class Query(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: Query):
    result = agent.run(query.question)
    return {"response": result}
