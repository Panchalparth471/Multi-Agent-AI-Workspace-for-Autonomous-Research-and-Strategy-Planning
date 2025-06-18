from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os

def get_report_chain():
    prompt = PromptTemplate.from_template(
        """
        Based on the following research and planning context, write a comprehensive strategic report.

        Research:
        {research}

        Plan:
        {plan}

        Ensure clarity, structure, and actionable recommendations.
        """
    )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192"
    )

    return LLMChain(llm=llm, prompt=prompt)