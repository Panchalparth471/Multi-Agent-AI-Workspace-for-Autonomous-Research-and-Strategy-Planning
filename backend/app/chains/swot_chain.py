from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os

def get_swot_chain():
    prompt = PromptTemplate.from_template(
        """
        Perform a SWOT analysis based on the following content:

        {input}

        Return the analysis in bullet format with headings for Strengths, Weaknesses, Opportunities, and Threats.
        """
    )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192"
    )

    return LLMChain(llm=llm, prompt=prompt)