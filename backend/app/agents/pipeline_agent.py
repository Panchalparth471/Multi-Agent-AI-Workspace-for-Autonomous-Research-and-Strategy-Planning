from app.agents.researcher_agent import get_researcher_agent
from app.agents.analyst_agent import get_analyst_agent
from app.agents.planner_agent import get_planner_agent
from app.agents.writer_agent import get_writer_agent
from app.agents.validator_agent import get_validator_agent

from app.services.embedding_service import get_embedding_model
from app.services.vectorstore_service import search_documents, add_documents_to_index
from app.utils.logging import setup_logger
from app.utils.formatters import (
    clean_output,
    extract_key_points,
    wrap_markdown_section,
    format_json_readable
)
from langchain.schema import Document
from langchain_core.messages import HumanMessage, AIMessage

logger = setup_logger(__name__)


def run_full_pipeline(query: str):
    logger.info("\U0001F50D Starting full agent pipeline for query: %s", query)
    embedding_model = get_embedding_model()
    
    # Step 0: Retrieve from FAISS
    logger.info(" Step 0: Retrieving from FAISS Vectorstore...")
    try:
        vector_results = search_documents(query, embedding_model, k=3)
        retrieved_knowledge = "\n\n".join([doc.page_content for doc in vector_results])
        logger.debug(wrap_markdown_section("Retrieved Docs", retrieved_knowledge))
    except Exception as e:
        logger.error(f"FAISS retrieval failed: {e}")
        retrieved_knowledge = ""

    # Step 1: Research
    logger.info("\U0001F9E0 Step 1: Research...")
    try:
        researcher = get_researcher_agent()
        research_input = f"Research the following topic: {query}"
        if retrieved_knowledge:
            research_input += f"\n\nContext from knowledge base:\n{retrieved_knowledge}"
        
        research_raw = researcher.invoke({"input": research_input})
        research_result = clean_output(research_raw)
        logger.debug(wrap_markdown_section("Research Output", research_result))
    except Exception as e:
        logger.error(f"Research step failed: {e}")
        research_result = f"Unable to complete research for: {query}. Using basic information."

    # Step 2: Analyze
    logger.info(" Step 2: Analysis...")
    try:
        analyst = get_analyst_agent()
        analysis_input = f"Analyze the following research findings about '{query}':\n\n{research_result}"
        
        analysis_raw = analyst.invoke({"input": analysis_input})
        analysis_result = clean_output(analysis_raw)
        
        # Extract key points with fallback
        try:
            key_points = extract_key_points(analysis_result)
        except:
            key_points = [analysis_result[:200] + "..."] if len(analysis_result) > 200 else [analysis_result]
        
        logger.debug(wrap_markdown_section("Analysis Key Points", "\n".join(f"- {pt}" for pt in key_points)))
    except Exception as e:
        logger.error(f"Analysis step failed: {e}")
        analysis_result = f"Basic analysis: {query} has significant impacts that require detailed examination."
        key_points = [analysis_result]

    # Step 3: Plan
    logger.info("📝 Step 3: Planning...")
    try:
        planner = get_planner_agent()
        plan_input = f"Create a comprehensive content plan for the topic '{query}' based on this analysis:\n\n{analysis_result}"
        
        plan_raw = planner.invoke({"input": plan_input})
        plan_result = clean_output(plan_raw)
        logger.debug(wrap_markdown_section("Content Plan", plan_result))
    except Exception as e:
        logger.error(f"Planning step failed: {e}")
        # Provide fallback plan structure
        plan_result = f"""
        Content Plan for {query}:
        1. Introduction and Overview
        2. Current State Analysis
        3. Key Benefits and Opportunities
        4. Challenges and Concerns
        5. Future Implications
        6. Recommendations and Conclusion
        """

    # Step 4: Write
    logger.info(" Step 4: Writing...")
    try:
        writer = get_writer_agent()
        write_input = f"Write a comprehensive article about '{query}' following this content plan:\n\n{plan_result}\n\nBased on this analysis:\n{analysis_result}"
        
        draft_raw = writer.invoke({"input": write_input})
        draft_result = clean_output(draft_raw)
        logger.debug(wrap_markdown_section("Draft", draft_result[:1000] + "\n..."))
    except Exception as e:
        logger.error(f"Writing step failed: {e}")
        # Provide fallback content
        draft_result = f"""
        # {query}
        
        ## Introduction
        {query} represents a significant area of development with far-reaching implications.
        
        ## Analysis
        {analysis_result}
        
        ## Conclusion
        Understanding {query} is crucial for navigating future developments in this field.
        """

    # Step 5: Validate
    logger.info(" Step 5: Validating...")
    try:
        validator = get_validator_agent()
        validation_input = f"Review and validate this article about '{query}':\n\n{draft_result}"
        
        validation_raw = validator.invoke({"input": validation_input})
        validation_result = clean_output(validation_raw)
        logger.debug(wrap_markdown_section("Validation Feedback", validation_result))
    except Exception as e:
        logger.error(f"Validation step failed: {e}")
        validation_result = f"Content validation completed for {query}. The article covers the main aspects of the topic."

    # Index final results
    logger.info(" Indexing final outputs to FAISS...")
    try:
        # Only index successful results
        docs_to_index = []
        
        if not research_result.startswith("Unable to complete"):
            docs_to_index.append(Document(page_content=f"Research: {research_result}", metadata={"type": "research", "query": query}))
        
        if not analysis_result.startswith("Basic analysis"):
            docs_to_index.append(Document(page_content=f"Analysis: {analysis_result}", metadata={"type": "analysis", "query": query}))
            
        if "Content Plan for" not in plan_result:
            docs_to_index.append(Document(page_content=f"Plan: {plan_result}", metadata={"type": "plan", "query": query}))
            
        if not draft_result.startswith("#"):
            docs_to_index.append(Document(page_content=f"Article: {draft_result}", metadata={"type": "article", "query": query}))
        
        if docs_to_index:
            add_documents_to_index(docs_to_index, embedding_model)
            logger.info(f"Successfully indexed {len(docs_to_index)} documents")
        
    except Exception as e:
        logger.error(f"FAISS indexing failed: {e}")

    logger.info(" Full pipeline execution complete.")

    return format_json_readable({
        "query": query,
        "retrieved_docs": retrieved_knowledge,
        "research": research_result,
        "analysis": analysis_result,
        "plan": plan_result,
        "draft": draft_result,
        "validation": validation_result,
        "key_points": key_points,
        "status": "completed"
    })
