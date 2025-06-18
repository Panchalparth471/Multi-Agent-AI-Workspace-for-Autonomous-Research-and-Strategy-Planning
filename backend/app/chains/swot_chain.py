from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os

def get_swot_chain():
    prompt = PromptTemplate.from_template(
        """
        Perform a comprehensive SWOT analysis based on the following content:

        {input}

        Analyze and categorize findings into:
        
        **STRENGTHS:**
        - Internal positive factors
        - Competitive advantages
        - Core competencies
        - Unique resources or capabilities
        
        **WEAKNESSES:**
        - Internal limitations
        - Areas for improvement
        - Resource constraints
        - Skill gaps
        
        **OPPORTUNITIES:**
        - External positive factors
        - Market trends
        - Emerging technologies
        - Partnership possibilities
        
        **THREATS:**
        - External challenges
        - Competitive pressures
        - Market risks
        - Regulatory concerns

        Return the analysis in clear bullet format with detailed explanations for each point.
        """
    )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192",
        temperature=0.2  # Lower temperature for analytical precision
    )

    return LLMChain(llm=llm, prompt=prompt)
