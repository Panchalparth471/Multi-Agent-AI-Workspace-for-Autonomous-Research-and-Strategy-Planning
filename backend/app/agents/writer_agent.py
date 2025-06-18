# agents/writer_agent.py
import os
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from app.tools.write_tool import get_write_tool

def get_writer_agent():
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192"
    )
    tools = [get_write_tool()]

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,  # ✅ ADDED
        verbose=True,
        max_iterations=3,  # ✅ ADDED
        early_stopping_method="generate"  # ✅ ADDED
    )