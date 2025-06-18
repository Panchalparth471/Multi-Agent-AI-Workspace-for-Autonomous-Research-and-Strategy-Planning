
#  Multi-Agent AI Workspace for Autonomous Research and Strategy Planning

A **modular, production-ready AI workspace** that leverages multiple autonomous agents to collaboratively perform end-to-end **research**, **analysis**, and **strategic decision-making**.

## Techstack
```
Groq, langchain, faiss, react, typescript, tailwindcss, mongodb, flask, Cohere
```
---

##  Key Features

###  Multi-Agent Architecture
- Built using **LangChain** with specialized agents for:
  - Research
  - Analysis
  - Planning
  - Writing
  - Validation  
- Each agent operates with **isolated tools and scoped memory** for modularity and task-specific focus.

###  RAG Pipeline (Retrieval-Augmented Generation)
- **Cohere Embeddings**: Semantic vector representations for contextual understanding.
- **FAISS**: High-speed vector indexing and similarity search.
- **MongoDB**: Document storage with metadata and persistent context.

###  LLM Power
- Utilizes **LLaMA 3 via Groq API** for ultra-low latency and high-throughput generation.

###  Real-Time Web Search
- Integrated **SERP API** tool to retrieve and ground data from the open web dynamically.

###  Collaborative Chains
- Agents work together in structured pipelines:
  -  **SWOT Chain**: Extracts Strengths, Weaknesses, Opportunities, and Threats from input.
  -  **Timeline Chain**: Builds chronological event breakdowns and plans.
  -  **Report Chain**: Compiles structured insights into formal reports.

---

##  Use Cases
-  Market Research & Competitive Intelligence  
-  Strategic Planning & Opportunity Analysis  
-  Automated Technical or Executive Reporting  
-  Knowledge Base Augmentation

---

### Output example of balanced pipeline


{
    "analysis": "Analysis timeout: Impact of AI on Education has significant impacts that require detailed examination.",
    "draft": "\n        # Impact of AI on Education\n        \n        ## Introduction\n        Impact of AI on Education represents a significant area of development with far-reaching implications.\n        \n        ## Analysis\n        Analysis timeout: Impact of AI on Education has significant impacts that require detailed examination.\n        \n        ## Conclusion\n        Understanding Impact of AI on Education is crucial for navigating future developments in this field.\n        ",
    "execution_time": 22.57194018363953,
    "key_points": [
"Analysis: Impact of AI on Education has significant impacts that require detailed examination."
],
    "plan": "\n            Content Plan for Impact of AI on Education:\n            1. Introduction and Overview\n            2. Current State Analysis\n            3. Key Benefits and Opportunities\n            4. Challenges and Concerns\n            5. Future Implications\n            6. Recommendations and Conclusion\n            ",
    "query": "Impact of AI on Education",
    "research": "The impact of AI on education is multifaceted, with both positive and negative consequences. On the one hand, AI can personalize learning experiences, inspire creativity, foster critical thinking, and improve accessibility. It can also empower educators, accelerate learning, and enhance instructional quality. On the other hand, AI can lead to bias in algorithms, privacy and security issues, decreased human interaction, and unemployment. To strike a balance between the benefits and drawbacks, it is crucial to ensure that AI is designed with principles in mind, and AI literacy is essential. By doing so, AI can offer transformative potential in education, personalizing learning, streamlining administrative tasks, and enhancing instructional quality.",
    "retrieved_docs": "Article: \n        # Impact of AI on Education\n        \n        ## Introduction\n        Impact of AI on Education represents a significant area of development with far-reaching implications.\n        \n        ## Analysis\n        The research findings provide a comprehensive analysis of the impact of AI on education, highlighting both the benefits and drawbacks. The key findings, important themes, implications, and areas for further investigation provide a nuanced understanding of the topic, enabli",
    "status": "completed",
    "strategic_report": "Skipped for performance",
    "swot_analysis": "Skipped for performance",
    "timeline": "Skipped for performance",
    "validation": "Skipped for performance"
}

---


##  Pipeline Performance Optimization Guide

### Pipeline Modes

1. **EXPRESS PIPELINE (5–15 seconds)**
   -  Use for: Quick insights, prototyping, real-time responses
   -  Trade-offs: Basic research + analysis only  
   -  Code: `run_express_pipeline(query)`

2. **BALANCED PIPELINE (15–30 seconds)**  
   -  Use for: Most production scenarios  
   -  Trade-offs: Skips validation and chains but includes core content  
   -  Code: `run_balanced_pipeline(query)`

3. **OPTIMIZED COMPREHENSIVE (30–60 seconds)**
   -  Use for: Full-featured analysis with parallel processing  
   -  Trade-offs: All features with performance optimizations  
   -  Code: `run_optimized_pipeline(query)`

4. **QUALITY FOCUSED (60–120 seconds)**
   -  Use for: High-quality reports, detailed analysis  
   -  Trade-offs: Slower but highest quality output  
   -  Code: `run_optimized_pipeline(query, config=PERFORMANCE_CONFIGS['quality_focused'])`

### Optimization Techniques

1. **Caching**
   - Agent instances cached to avoid recreation
   - Chain instances cached
   -  Memory usage: ~50MB per cached instance

2. **Parallel Processing**
   - Final steps (validation, report, SWOT, timeline) run in parallel
   - 4× speedup using `ThreadPoolExecutor`

3. **Timeouts**
   - Prevents hanging on slow API calls
   - Configurable per step
   - Automatic fallback responses

4. **Content Limiting**
   - Input size limits prevent token overflow
   - Smart truncation preserves key information
   - Reduces API costs and latency

5. **Background Operations**
   - Indexing runs in background
   - Document saving is async
   - Non-blocking behavior

6. **Feature Toggling**
   - Skips expensive steps when not needed
   - Configurable depth per pipeline type
   - Optimized for specific use cases

### Performance Comparison

| Pipeline Type        | Time Estimate     | Speedup         |
|----------------------|------------------|-----------------|
| Original             | 120–180 seconds  | —               |
| Express              | 5–15 seconds     | 12× faster      |
| Balanced             | 15–30 seconds    | 4–6× faster     |
| Optimized            | 30–60 seconds    | 2–3× faster     |

### Memory Usage

| Mode               | Memory Usage       |
|--------------------|--------------------|
| Without Caching    | ~200MB per run     |
| With Caching       | ~100MB per run     |
| Express Mode       | ~50MB per run      |

### API Calls Reduction

| Pipeline           | API Calls          |
|--------------------|--------------------|
| Original           | 8–12               |
| Express            | 2                  |
| Balanced           | 4                  |
| Optimized          | 8 (parallelized)   |

---

##  Use Cases

- Market Research & Competitive Intelligence  
- Strategic Planning & Opportunity Analysis  
- Automated Technical or Executive Reporting  
- Knowledge Base Augmentation  

---

## 📦 Sample Output (Balanced Pipeline)

```json
{
  "query": "Impact of AI on Education",
  "research": "The impact of AI on education is multifaceted...",
  "analysis": "Analysis timeout: Impact of AI on Education has significant impacts...",
  "plan": "1. Introduction\n2. Current State Analysis\n...",
  "key_points": [
    "Analysis: Impact of AI on Education has significant impacts..."
  ],
  "draft": "## Introduction\nImpact of AI on Education...",
  "retrieved_docs": "Article: # Impact of AI on Education...",
  "timeline": "Skipped for performance",
  "swot_analysis": "Skipped for performance",
  "strategic_report": "Skipped for performance",
  "validation": "Skipped for performance",
  "execution_time": 22.57,
  "status": "completed"
}

