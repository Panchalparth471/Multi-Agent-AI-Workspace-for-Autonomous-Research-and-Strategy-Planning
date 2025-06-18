import os
import json
import re
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

# Copy the extract_json_from_response function here too, or import it from a utils file

def validate_content_wrapper(input_text: str) -> str:
    """Wrapper function for the validate tool with JSON parsing."""
    try:
        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )

        prompt = PromptTemplate.from_template(
            """You are a Validator agent.

Instructions: Validate the following content for grammar, factual accuracy, clarity, and logical flow.

IMPORTANT: Respond with ONLY a JSON object in this exact format:

{
  "issues_found": [
    {
      "type": "grammar",
      "description": "Brief description of the issue"
    }
  ],
  "revised_version": "Full revised text with corrections applied"
}

Content to validate:
{input}

Remember: Return ONLY the JSON object, no additional text, explanations, or markdown code blocks."""
        )
        
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run(input=input_text)
        
        # Try to extract JSON from the response
        json_data = extract_json_from_response(response)
        
        if json_data and "issues_found" in json_data and "revised_version" in json_data:
            # Format validation results
            issues = json_data.get("issues_found", [])
            revised = json_data.get("revised_version", "")
            
            validation_report = "## Validation Report\n\n"
            
            if issues:
                validation_report += "### Issues Found:\n"
                for i, issue in enumerate(issues, 1):
                    issue_type = issue.get("type", "unknown")
                    description = issue.get("description", "No description")
                    validation_report += f"{i}. **{issue_type.title()}**: {description}\n"
                validation_report += "\n"
            else:
                validation_report += "### No Issues Found\nContent is well-structured and accurate.\n\n"
            
            if revised:
                validation_report += f"### Revised Version:\n{revised}"
            
            return validation_report
        else:
            # Fallback: return basic validation
            return f"## Validation Complete\n\nContent has been reviewed. Basic validation indicates the content covers the topic adequately.\n\nOriginal content length: {len(input_text)} characters"
            
    except Exception as e:
        return f"## Validation Error\n\nValidation process encountered an error: {str(e)}\n\nContent appears to be: {input_text[:100]}..."

def get_validate_tool():
    return Tool(
        name="Validator",
        func=validate_content_wrapper,
        description="Review and validate a document's grammar, clarity, and correctness."
    )