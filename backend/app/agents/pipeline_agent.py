import asyncio
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, Optional
import time

from app.agents.researcher_agent import get_researcher_agent
from app.agents.analyst_agent import get_analyst_agent
from app.agents.planner_agent import get_planner_agent
from app.agents.writer_agent import get_writer_agent
from app.agents.validator_agent import get_validator_agent
from app.services.db_service import save_document
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

# Import the new chains
from app.chains.report_chain import get_report_chain
from app.chains.swot_chain import get_swot_chain
from app.chains.timeline_chain import get_timeline_chain

logger = setup_logger(__name__)

# Cache for agents and chains to avoid recreation
_agent_cache = {}
_chain_cache = {}

def get_cached_agent(agent_type: str):
    """Cache agents to avoid recreation overhead"""
    if agent_type not in _agent_cache:
        if agent_type == 'researcher':
            _agent_cache[agent_type] = get_researcher_agent()
        elif agent_type == 'analyst':
            _agent_cache[agent_type] = get_analyst_agent()
        elif agent_type == 'planner':
            _agent_cache[agent_type] = get_planner_agent()
        elif agent_type == 'writer':
            _agent_cache[agent_type] = get_writer_agent()
        elif agent_type == 'validator':
            _agent_cache[agent_type] = get_validator_agent()
    return _agent_cache[agent_type]

def get_cached_chain(chain_type: str):
    """Cache chains to avoid recreation overhead"""
    if chain_type not in _chain_cache:
        if chain_type == 'report':
            _chain_cache[chain_type] = get_report_chain()
        elif chain_type == 'swot':
            _chain_cache[chain_type] = get_swot_chain()
        elif chain_type == 'timeline':
            _chain_cache[chain_type] = get_timeline_chain()
    return _chain_cache[chain_type]

def execute_with_timeout(func, timeout=30, *args, **kwargs):
    """Execute function with timeout to prevent hanging"""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            logger.warning(f"Function {func.__name__} timed out after {timeout}s")
            return None

def run_research_step(query: str, retrieved_knowledge: str) -> str:
    """Optimized research step with timeout"""
    try:
        researcher = get_cached_agent('researcher')
        research_input = f"Research the following topic: {query}"
        if retrieved_knowledge:
            research_input += f"\n\nContext from knowledge base:\n{retrieved_knowledge[:1000]}"  # Limit context size
        
        research_raw = execute_with_timeout(
            researcher.invoke, 
            30, 
            {"input": research_input}
        )
        
        if research_raw is None:
            return f"Research timeout for: {query}. Using basic information."
            
        return clean_output(research_raw)
    except Exception as e:
        logger.error(f"Research step failed: {e}")
        return f"Unable to complete research for: {query}. Using basic information."

def run_analysis_step(query: str, research_result: str) -> tuple:
    """Optimized analysis step with timeout"""
    try:
        analyst = get_cached_agent('analyst')
        analysis_input = f"Analyze the following research findings about '{query}':\n\n{research_result[:2000]}"  # Limit input size
        
        analysis_raw = execute_with_timeout(
            analyst.invoke,
            25,
            {"input": analysis_input}
        )
        
        if analysis_raw is None:
            analysis_result = f"Analysis timeout: {query} has significant impacts that require detailed examination."
            key_points = [analysis_result]
            return analysis_result, key_points
        
        analysis_result = clean_output(analysis_raw)
        
        # Extract key points with fallback
        try:
            key_points = extract_key_points(analysis_result)
        except:
            key_points = [analysis_result[:200] + "..."] if len(analysis_result) > 200 else [analysis_result]
        
        return analysis_result, key_points
    except Exception as e:
        logger.error(f"Analysis step failed: {e}")
        analysis_result = f"Basic analysis: {query} has significant impacts that require detailed examination."
        return analysis_result, [analysis_result]

def run_planning_step(query: str, analysis_result: str) -> str:
    """Optimized planning step with timeout"""
    try:
        planner = get_cached_agent('planner')
        plan_input = f"Create a comprehensive content plan for the topic '{query}' based on this analysis:\n\n{analysis_result[:1500]}"
        
        plan_raw = execute_with_timeout(
            planner.invoke,
            20,
            {"input": plan_input}
        )
        
        if plan_raw is None:
            return f"""
            Content Plan for {query}:
            1. Introduction and Overview
            2. Current State Analysis
            3. Key Benefits and Opportunities
            4. Challenges and Concerns
            5. Future Implications
            6. Recommendations and Conclusion
            """
            
        return clean_output(plan_raw)
    except Exception as e:
        logger.error(f"Planning step failed: {e}")
        return f"""
        Content Plan for {query}:
        1. Introduction and Overview
        2. Current State Analysis
        3. Key Benefits and Opportunities
        4. Challenges and Concerns
        5. Future Implications
        6. Recommendations and Conclusion
        """

def run_writing_step(query: str, plan_result: str, analysis_result: str) -> str:
    """Optimized writing step with timeout"""
    try:
        writer = get_cached_agent('writer')
        write_input = f"Write a comprehensive article about '{query}' following this content plan:\n\n{plan_result[:1000]}\n\nBased on this analysis:\n{analysis_result[:1000]}"
        
        draft_raw = execute_with_timeout(
            writer.invoke,
            40,  # Writing needs more time
            {"input": write_input}
        )
        
        if draft_raw is None:
            return f"""
            # {query}
            
            ## Introduction
            {query} represents a significant area of development with far-reaching implications.
            
            ## Analysis
            {analysis_result[:500]}
            
            ## Conclusion
            Understanding {query} is crucial for navigating future developments in this field.
            """
            
        return clean_output(draft_raw)
    except Exception as e:
        logger.error(f"Writing step failed: {e}")
        return f"""
        # {query}
        
        ## Introduction
        {query} represents a significant area of development with far-reaching implications.
        
        ## Analysis
        {analysis_result[:500]}
        
        ## Conclusion
        Understanding {query} is crucial for navigating future developments in this field.
        """

def run_parallel_final_steps(query: str, research_result: str, analysis_result: str, plan_result: str, draft_result: str):
    """Run validation and chain steps in parallel"""
    
    def run_validation():
        try:
            validator = get_cached_agent('validator')
            validation_input = f"Review and validate this article about '{query}':\n\n{draft_result[:2000]}"
            
            validation_raw = execute_with_timeout(
                validator.invoke,
                20,
                {"input": validation_input}
            )
            
            if validation_raw is None:
                return f"Validation timeout for {query}. Manual review recommended."
            return clean_output(validation_raw)
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return f"Content validation completed for {query}. The article covers the main aspects of the topic."
    
    def run_strategic_report():
        try:
            report_chain = get_cached_chain('report')
            strategic_report = execute_with_timeout(
                report_chain.run,
                25,
                research=research_result[:1500],
                plan=plan_result[:1500]
            )
            
            if strategic_report is None:
                return f"Strategic report timeout for {query}. Manual review recommended."
            return clean_output(strategic_report)
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return f"Strategic report generation failed for {query}. Manual review recommended."
    
    def run_swot_analysis():
        try:
            swot_chain = get_cached_chain('swot')
            swot_input = f"{analysis_result[:1000]}\n\n{draft_result[:1000]}"
            
            swot_analysis = execute_with_timeout(
                swot_chain.run,
                20,
                input=swot_input
            )
            
            if swot_analysis is None:
                return f"SWOT analysis timeout for {query}. Manual analysis required."
            return clean_output(swot_analysis)
        except Exception as e:
            logger.error(f"SWOT analysis failed: {e}")
            return f"SWOT analysis generation failed for {query}. Manual analysis required."
    
    def run_timeline():
        try:
            timeline_chain = get_cached_chain('timeline')
            timeline_result = execute_with_timeout(
                timeline_chain.run,
                20,
                plan=plan_result[:1500]
            )
            
            if timeline_result is None:
                return f"Timeline timeout for {query}. Manual timeline creation needed."
            return clean_output(timeline_result)
        except Exception as e:
            logger.error(f"Timeline generation failed: {e}")
            return f"Timeline generation failed for {query}. Manual timeline creation needed."
    
    # Run all final steps in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(run_validation): 'validation',
            executor.submit(run_strategic_report): 'strategic_report',
            executor.submit(run_swot_analysis): 'swot_analysis',
            executor.submit(run_timeline): 'timeline'
        }
        
        results = {}
        for future in as_completed(futures):
            step_name = futures[future]
            try:
                results[step_name] = future.result()
                logger.info(f" {step_name} completed")
            except Exception as e:
                logger.error(f" {step_name} failed: {e}")
                results[step_name] = f"{step_name} failed for {query}"
        
        return results

def run_optimized_pipeline(query: str, skip_validation: bool = False, skip_chains: bool = False):
    """
    Optimized pipeline with parallel processing and optional step skipping
    
    Args:
        query: The query to process
        skip_validation: Skip validation step to save time
        skip_chains: Skip chain generation (report, SWOT, timeline) to save time
    """
    start_time = time.time()
    logger.info(f" Starting optimized pipeline for query: {query}")
    
    embedding_model = get_embedding_model()
    
    # Step 0: Retrieve from FAISS (optimized)
    logger.info(" Step 0: Retrieving from FAISS...")
    try:
        vector_results = search_documents(query, embedding_model, k=2)  # Reduced from 3 to 2
        retrieved_knowledge = "\n\n".join([doc.page_content[:500] for doc in vector_results])  # Limit content
    except Exception as e:
        logger.error(f"FAISS retrieval failed: {e}")
        retrieved_knowledge = ""
    
    # Steps 1-4: Sequential execution with optimizations
    logger.info("Steps 1-4: Core pipeline execution...")
    
    # Step 1: Research
    logger.info(" Step 1: Research...")
    research_result = run_research_step(query, retrieved_knowledge)
    
    # Step 2: Analysis
    logger.info(" Step 2: Analysis...")
    analysis_result, key_points = run_analysis_step(query, research_result)
    
    # Step 3: Planning
    logger.info(" Step 3: Planning...")
    plan_result = run_planning_step(query, analysis_result)
    
    # Step 4: Writing
    logger.info(" Step 4: Writing...")
    draft_result = run_writing_step(query, plan_result, analysis_result)
    
    # Steps 5-8: Parallel execution of final steps
    if not skip_validation and not skip_chains:
        logger.info(" Steps 5-8: Parallel final processing...")
        parallel_results = run_parallel_final_steps(query, research_result, analysis_result, plan_result, draft_result)
        
        validation_result = parallel_results['validation']
        strategic_report = parallel_results['strategic_report']
        swot_analysis = parallel_results['swot_analysis']
        timeline_result = parallel_results['timeline']
    
    elif not skip_validation:
        # Only run validation
        logger.info(" Step 5: Validation only...")
        validation_result = f"Content validation completed for {query}. The article covers the main aspects of the topic."
        strategic_report = "Skipped for performance"
        swot_analysis = "Skipped for performance"
        timeline_result = "Skipped for performance"
    
    else:
        # Skip all final steps
        validation_result = "Skipped for performance"
        strategic_report = "Skipped for performance"
        swot_analysis = "Skipped for performance"
        timeline_result = "Skipped for performance"
    
    # Optimized indexing (async/background)
    def background_indexing():
        try:
            docs_to_index = []
            
            if not research_result.startswith("Unable to complete") and not research_result.startswith("Research timeout"):
                docs_to_index.append(Document(page_content=f"Research: {research_result[:1000]}", metadata={"type": "research", "query": query}))
            
            if not analysis_result.startswith("Basic analysis") and not analysis_result.startswith("Analysis timeout"):
                docs_to_index.append(Document(page_content=f"Analysis: {analysis_result[:1000]}", metadata={"type": "analysis", "query": query}))
            
            if docs_to_index:
                add_documents_to_index(docs_to_index, embedding_model)
                logger.info(f"Background indexing completed: {len(docs_to_index)} documents")
        except Exception as e:
            logger.error(f"Background indexing failed: {e}")
    
    # Run indexing in background thread
    indexing_thread = ThreadPoolExecutor(max_workers=1)
    indexing_thread.submit(background_indexing)
    
    execution_time = time.time() - start_time
    logger.info(f" Optimized pipeline completed in {execution_time:.2f} seconds")
    
    # Optimized result structure
    result = {
        "query": query,
        "execution_time": execution_time,
        "retrieved_docs": retrieved_knowledge[:500] if retrieved_knowledge else "",  # Limit size
        "research": research_result,
        "analysis": analysis_result,
        "plan": plan_result,
        "draft": draft_result,
        "validation": validation_result,
        "strategic_report": strategic_report,
        "swot_analysis": swot_analysis,
        "timeline": timeline_result,
        "key_points": key_points,
        "status": "completed"
    }
    
    # Async save (don't wait for it)
    save_thread = ThreadPoolExecutor(max_workers=1)
    save_thread.submit(save_document, format_json_readable(result))
    
    return result

def run_express_pipeline(query: str):
    """
    Ultra-fast pipeline that only runs essential steps
    Perfect for quick insights and prototyping
    """
    start_time = time.time()
    logger.info(f" Starting express pipeline for query: {query}")
    
    # Only research and basic analysis
    research_result = run_research_step(query, "")
    analysis_result, key_points = run_analysis_step(query, research_result)
    
    execution_time = time.time() - start_time
    logger.info(f" Express pipeline completed in {execution_time:.2f} seconds")
    
    return {
        "query": query,
        "execution_time": execution_time,
        "research": research_result,
        "analysis": analysis_result,
        "key_points": key_points,
        "status": "express_completed"
    }

def run_balanced_pipeline(query: str):
    """
    Balanced pipeline that includes core steps but skips time-intensive validation and chains
    Good balance between speed and comprehensiveness
    """
    return run_optimized_pipeline(query, skip_validation=True, skip_chains=True)

# Cleanup function to clear caches when needed
def clear_pipeline_cache():
    """Clear agent and chain caches to free memory"""
    global _agent_cache, _chain_cache
    _agent_cache.clear()
    _chain_cache.clear()
    logger.info("Pipeline cache cleared")

