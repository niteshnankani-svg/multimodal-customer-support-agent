# 🤖 Multimodal AI Customer Support Agent

An intelligent customer support system that processes **both product images and complaint text simultaneously** using GPT-4V — a true multimodal AI application.

🔴 **Live Demo**: [huggingface.co/spaces/nitz0219/multimodal-customer-support-agent](https://huggingface.co/spaces/nitz0219/multimodal-customer-support-agent)

---

## 🧠 What It Does

Upload a photo of a damaged/wrong product + describe your complaint in text. The AI reads **both inputs together** and generates an intelligent resolution — just like a human support agent would.

---

## 🏗️ Architecture

```
User Input (Image + Text)
        ↓
   Gradio Frontend
        ↓
   FastAPI Backend
        ↓
  Redis Cache Check
  ┌────────────────┐
  │ Cache HIT?     │ → Return instantly (free + fast)
  │ Cache MISS?    │ → Call GPT-4V
  └────────────────┘
        ↓
   GPT-4V Analysis
   (Image + Text → Response)
        ↓
  Save to Redis Cache
        ↓
  Save to SQLite Database
        ↓
  Return Response to User
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Model | OpenAI GPT-4V (multimodal) |
| Frontend | Gradio |
| Backend | FastAPI |
| Caching | Redis |
| Database | SQLite |
| Deployment | Docker + Hugging Face Spaces |

---

## 🚀 System Design Features

- **Load Balancing** — handles multiple concurrent users
- **Redis Caching** — same complaint type returns instantly (1 hour TTL)
- **SQLite Database** — every complaint + response saved permanently
- **Docker** — fully containerized for production deployment

---

## 📦 Installation

```bash
git clone https://github.com/niteshnankani-svg/multimodal-customer-support-agent
cd multimodal-customer-support-agent
pip install -r requirements.txt
```

Create `.env` file:
```
OPENAI_API_KEY=your_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
```

Run:
```bash
docker-compose up
python frontend/gradio_app.py
```

---

## 🎯 Use Cases

- Ecommerce customer support (Flipkart, Amazon, Meesho)
- Product quality inspection
- Insurance claim processing
- Manufacturing defect reporting

---

## 👨‍💻 Author

**Nitesh Nankani** — AI/ML Engineer  
[HuggingFace](https://huggingface.co/nitz0219) | [GitHub](https://github.com/niteshnankani-svg) | [LinkedIn](https://linkedin.com/in/niteshnankani)
