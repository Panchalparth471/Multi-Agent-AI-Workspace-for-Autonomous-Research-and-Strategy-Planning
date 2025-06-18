# agents/validator_agent.py
import os
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from app.tools.validate_tool import get_validate_tool

def get_validator_agent():
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192"
    )
    tools = [get_validate_tool()]

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True, 
        verbose=True,
        max_iterations=3, 
        early_stopping_method="generate"  
    )
