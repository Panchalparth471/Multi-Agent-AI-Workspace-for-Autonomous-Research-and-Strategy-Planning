import os
import json
import re
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

def extract_json_from_response(response: str) -> dict:
    """Extract JSON from LLM response that might contain markdown code blocks."""
    try:
        # First try to parse as direct JSON
        return json.loads(response.strip())
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to extract JSON without markdown
        json_match = re.search(r'(\{.*\})', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
    
    return None

def write_content_wrapper(input_text: str) -> str:
    """Wrapper function for the write tool with JSON parsing."""
    try:
        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )

        prompt = PromptTemplate.from_template(
            """You are a professional writer.

Task: Based on the following content plan, draft a detailed, coherent, and well-structured article or report.

IMPORTANT: Respond with ONLY a JSON object in this exact format:

{
  "title": "Title of the article/report",
  "body": "Full article/report text with proper formatting and structure"
}

Content plan:
{input}

Remember: Return ONLY the JSON object, no additional text, explanations, or markdown code blocks."""
        )
        
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run(input=input_text)
        
        # Try to extract JSON from the response
        json_data = extract_json_from_response(response)
        
        if json_data and "title" in json_data and "body" in json_data:
            # Format as a readable article
            formatted_content = f"# {json_data['title']}\n\n{json_data['body']}"
            return formatted_content
        else:
            # Fallback: return the raw response
            return f"# Article Draft\n\n{response}"
            
    except Exception as e:
        return f"# Content Writing Error\n\nUnable to generate content: {str(e)}\n\nFallback content based on: {input_text[:100]}..."

def get_write_tool():
    return Tool(
        name="Writer",
        func=write_content_wrapper,
        description="Draft content from a given plan using an LLM."
    )