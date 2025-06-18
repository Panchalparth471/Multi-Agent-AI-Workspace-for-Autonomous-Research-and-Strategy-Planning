from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os

def get_report_chain():
    prompt = PromptTemplate.from_template(
        """
        Based on the following research and planning context, write a comprehensive strategic report.
        
        Focus on:
        - Executive summary
        - Key findings and insights
        - Strategic recommendations
        - Risk assessment
        - Implementation considerations
        - Success metrics

        Research:
        {research}

        Plan:
        {plan}

        Ensure clarity, structure, and actionable recommendations. Format as a professional business report.
        """
    )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192",
        temperature=0.3  # Lower temperature for more structured output
    )

    return LLMChain(llm=llm, prompt=prompt)
