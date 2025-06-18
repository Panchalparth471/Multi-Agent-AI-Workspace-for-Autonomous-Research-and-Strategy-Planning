import os
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import json

def plan_content(input_text: str) -> str:
    """Create a structured content plan based on analysis insights."""
    try:
        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )

        prompt = PromptTemplate.from_template(
            """You are a Content Planning Expert.

Create a detailed, structured content plan based on the provided insights.

Instructions:
1. Analyze the input carefully
2. Create a comprehensive plan with clear sections
3. Each section should have specific objectives
4. Return your response as a well-structured plan

Input to analyze:
{input}

Please create a content plan with the following structure:
- Title: [Overall plan title]
- Section 1: [Title and objectives]
- Section 2: [Title and objectives]
- Section 3: [Title and objectives]
- Section 4: [Title and objectives]
- Section 5: [Title and objectives]

Make sure each section has clear objectives and flows logically."""
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(input=input_text)
        
        return result
        
    except Exception as e:
        return f"Content Planning Error: {str(e)}. Proceeding with basic plan structure."

def get_plan_tool():
    return Tool(
        name="Content Planner",
        func=plan_content,
        description="Creates a structured content plan based on analysis insights. Input should be analysis results or topic information."
    )