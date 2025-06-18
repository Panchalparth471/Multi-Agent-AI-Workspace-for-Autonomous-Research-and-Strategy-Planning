from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os

def get_timeline_chain():
    prompt = PromptTemplate.from_template(
        """
        Given the following plan, create a detailed quarterly timeline with key milestones, deliverables, and success criteria:

        {plan}

        Create a comprehensive timeline following this structure:

        **Q1 (Months 1-3):**
        - Key initiatives and milestones
        - Deliverables and outcomes
        - Success metrics
        - Resource requirements

        **Q2 (Months 4-6):**
        - Key initiatives and milestones
        - Deliverables and outcomes
        - Success metrics
        - Resource requirements

        **Q3 (Months 7-9):**
        - Key initiatives and milestones
        - Deliverables and outcomes
        - Success metrics
        - Resource requirements

        **Q4 (Months 10-12):**
        - Key initiatives and milestones
        - Deliverables and outcomes
        - Success metrics
        - Resource requirements

        Include dependencies between quarters and critical path items. Be specific and actionable.
        """
    )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192",
        temperature=0.1  # Very low temperature for structured planning
    )

    return LLMChain(llm=llm, prompt=prompt)

