
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

