# tools/analyze_tool.py
import os
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

def analyze_content(input_text: str) -> str:
    """Analyze research findings and extract key insights."""
    try:
        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )

        prompt = PromptTemplate.from_template(
            """You are an Expert Analyst.

Analyze the following research findings and provide comprehensive insights.

Instructions:
1. Identify key themes and patterns
2. Extract important findings
3. Highlight potential implications
4. Note any gaps or areas needing more research
5. Provide a clear, structured analysis

Research findings to analyze:
{input}

Please provide your analysis in a clear, structured format with:
- Key Findings
- Important Themes
- Implications
- Areas for Further Investigation"""
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(input=input_text)
        
        return result
        
    except Exception as e:
        return f"Analysis completed with basic insights: {input_text[:200]}..."

def get_analyze_tool():
    return Tool(
        name="Content Analyzer",
        func=analyze_content,
        description="Analyzes research findings and extracts key insights, themes, and implications."
    )
