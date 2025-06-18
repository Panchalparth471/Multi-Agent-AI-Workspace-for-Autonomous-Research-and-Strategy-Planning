from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os

def get_timeline_chain():
    prompt = PromptTemplate.from_template(
        """
        Given the following plan, create a quarterly timeline with key milestones:

        {plan}

        Output format:
        Q1: ...
        Q2: ...
        Q3: ...
        Q4: ...
        """
    )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192"
    )

    return LLMChain(llm=llm, prompt=prompt)