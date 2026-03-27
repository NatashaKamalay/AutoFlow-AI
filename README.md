# AutoFlow AI  
### Autonomous Multi-Agent Workflow Intelligence System
AutoFlow AI is a multi-agent system that transforms unstructured enterprise communication (meeting transcripts, documents) into structured, actionable workflows with built-in risk detection, escalation, and contextual knowledge retrieval.

## Problem Statement
Enterprise teams often rely on unstructured communication such as meetings, chats, and documents. This leads to:
- Missed action items
- Lack of accountability
- Poor workflow visibility
- Delayed execution due to hidden blockers

## Solution
AutoFlow AI uses a **multi-agent architecture** to:
- Extract actionable insights from unstructured data
- Convert them into structured tasks
- Validate workflow completeness
- Detect risks proactively
- Recommend escalation actions
- Enable follow-up Q&A using RAG

## System Architecture
The system consists of specialized agents:

### Extraction Agent
- Converts raw text into:
  - Summary
  - Tasks
  - Decisions
  - Blockers

### Decision Agent
- Assigns:
  - Priority
  - Status (`ready` / `at_risk`)

### Verification Agent
- Ensures:
  - Tasks have owners & deadlines
  - Workflow completeness

### Monitoring Agent
- Detects workflow risks:
  - Missing ownership
  - Execution blockers

### Escalation Agent
- Suggests corrective actions:
  - Manager review
  - Owner assignment

### RAG Knowledge Agent
- Uses embeddings + FAISS
- Enables contextual Q&A on uploaded content

## Workflow Pipeline
1. Input: Paste transcript or upload document  
2. Extract structured data  
3. Enrich tasks with priority & status  
4. Validate completeness  
5. Detect risks  
6. Generate escalation actions  
7. Build knowledge base (RAG)  
8. Answer follow-up questions  

## Features
-  Multi-agent architecture  
-  Document upload (PDF, DOCX, TXT)  
-  Task extraction & structuring  
-  Workflow validation  
-  Risk monitoring  
-  Escalation recommendations  
-  RAG-based question answering  
-  Interactive Streamlit dashboard
-  
## 📊 Example Use Case
Input: 
Priya will send the revised proposal by Monday.
Arun will review the pricing sheet by Tuesday.
Blocker: legal approval pending.


## Output:
- Tasks with owners & deadlines  
- Identified blocker  
- Risk analysis  
- Escalation suggestions  
- Follow-up Q&A support  

## Tech Stack
- Python  
- Streamlit  
- LangChain  
- Google Gemini API  
- FAISS (Vector Store)  
- Pandas / Matplotlib  

## Installation & Setup
### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AutoFlow-AI.git
cd AutoFlow-AI


