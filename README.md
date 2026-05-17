# Multimodal Customer Support Agent

> Production customer support agent that reads images — GPT-4V + Redis caching + full Docker deployment.

## Problem Statement
Most AI support bots are text-only, forcing customers to describe visual problems in words — a broken product, a damaged package, a UI bug screenshot. A multimodal agent that accepts images alongside text handles real-world support tickets as they actually arrive.

## Architecture
FastAPI receives support tickets as multimodal input (text + optional image). Images are base64-encoded and passed to GPT-4V, which analyzes visual context alongside the text query. Redis caches responses for repeated issue patterns (e.g., identical error screenshots). SQLite logs all interactions for audit and analytics. Gradio provides a drag-and-drop chat interface. Docker containerizes the full stack for one-command deployment.

## Tech Stack
`Python` · `GPT-4V (OpenAI)` · `FastAPI` · `Redis` · `SQLite` · `Gradio` · `Docker` · `HuggingFace Spaces`

## Key Results
- Accepts text + image tickets simultaneously
- Redis cache reduces API costs on repeated queries
- Full session logging to SQLite
- Deployed on HuggingFace Spaces

## Live Demo
🔗 [huggingface.co/spaces/nitz0219/multimodal-customer-support-agent](https://huggingface.co/spaces/nitz0219/multimodal-customer-support-agent)

## How to Run Locally
```bash
git clone https://github.com/niteshnankani-svg/multimodal-customer-support-agent
cd multimodal-customer-support-agent
cp .env.example .env          # add OPENAI_API_KEY
docker-compose up --build
# Open http://localhost:7860
```
