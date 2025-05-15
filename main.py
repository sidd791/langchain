from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from app.tools import greet_tool, time_tool
from app.prompts import intents
from app.models import ChatHistory
from database.db import get_session

app = FastAPI()

llm = OllamaLLM(model="llama2")

class UserQuery(BaseModel):
    question: str

def detect_intent(question: str) -> str:
    for intent, data in intents.items():
        for ex in data["examples"]:
            if ex.lower() in question.lower():
                return intent
    return "unknown"

def run_tools_for_intent(intent: str) -> str:
    tool_chain = intents.get(intent, {}).get("tools", [])
    output = []
    for tool in tool_chain:
        if tool == "greet_tool":
            output.append(greet_tool())
        elif tool == "time_tool":
            output.append(time_tool())
    return " ".join(output) if output else "Sorry, I don't know how to help with that."

@app.post("/chat")
async def chat(query: UserQuery):
    intent = detect_intent(query.question)
    tool_response = run_tools_for_intent(intent)
    prompt_template = PromptTemplate.from_template("User: {question}\nTools: {tool_response}\nAI:")
    final_prompt = prompt_template.format(question=query.question, tool_response=tool_response)
    ai_response = llm.invoke(final_prompt)

    session = get_session()
    chat = ChatHistory(
        user_message=query.question,
        bot_response=ai_response,
        intent=intent
    )
    session.add(chat)
    session.commit()

    return {
        "intent": intent,
        "tool_output": tool_response,
        "ai_response": ai_response
    }
