# About the project
## CrewAI Debate System
Multi agent debate system built using CrewAI.

The system:
- creates arguments for and against a topic
- validates both arguments
- judges the final debate
- Sends the result through email

## Features
- Multi agent debate workflow
- Web search integration using DDGS/SerpAPI
- Sequential task orchestration
- Argument validation/review phase
- Final judge decision with task delegation enablement
- Email sending using SendGrid

## Project Structure
crewai_debate/
├── src/
│   └── debate/
│       ├── crew.py
│       ├── main.py
│       ├── tools/
│       │   ├── web_search_tool.py
│       │   └── sendgrid_tool.py
│       └── config/
│           ├── agents.yaml
│           └── tasks.yaml
│
├── pyproject.toml
└── README.md

## Setup

## 1. Install CrewAI
- pip install crewai
Or
- uv pip install crewai (Recommended)

## 2. Install Dependencies
- uv add ddgs redis sendgrid serpapi

### Environment Variables
- Create `.env`
- OPENAI_API_KEY=your_openai_key
- SENDGRID_API_KEY=your_sendgrid_key
- OPENAI_BASE_URL=<>
- SERPAPI_API_KEY=your_serpapi_key

### Run The Project
crewai run

### Agents
- offline model is used here to SAVE COST
- use ollama and there are plenty of offline model available
- few names are:
    1. codestral:latest
    2. phi4:latest
    qwen3:8b
    mistral-nemo:latest
    llama3:8b          
    deepseek-r1:7b     
    deepseek-coder:6.7b
    gemma4:e4b

### supporting arguments
Creates supporting arguments to save context of agent execution

### Web Search Tool
Uses:
DDGS OR SerpAPI search
Cached searches avoid repeated web requests (Redis is used but code is commented for future enhancement)

### Example Workflow
Topic
  ↓
Supporting Argument
  ↓
Web search for fact-check
  ↓
Supporting Validation
  ↓
Opposing Argument
  ↓
Web search for fact-check
  ↓
Opposing Validation
  ↓
Final Judge Decision
  ↓
Send Email

# Useful Commands

### Install dependencies
crewai install

### Run crew
crewai run

### Notes

* `allow_delegation=False` is recommended unless autonomous delegation is required.
* Web search cache is shared through Redis.
* DDGS may occasionally fail due to provider instability or DNS/network issues (Use serpapi instead)
* CrewAI verbose logs can appear repetitive due to live progress rendering.

### Recommended Improvements

Future enhancements:
* Introduce Caching
* Semantic search caching
* Retry policies
* Observability/tracing
* Structured output validation
* Async execution
* Human review checkpoints
