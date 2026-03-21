# 🎯 CareerPilot — AI Career Advisor That Learns From Every Conversation

> An AI career mentor that remembers your skills, tracks your rejections, and gets smarter about your career path over time — powered by [Hindsight](https://github.com/vectorize-io/hindsight) agent memory.

## The Problem

Students struggle to track their evolving skills, internship applications, and career progress. Generic career advice doesn't account for your personal history — your specific skills, what you've been rejected from, and what you're actually interested in.

## The Solution

CareerPilot is an AI career advisor that **remembers everything** across conversations. Tell it about your Python skills today, your DataCorp rejection tomorrow, and next week it will proactively suggest data engineering roles that match your background while addressing the exact skill gaps that got you rejected.

### How Hindsight Memory Makes This Work

| Without Memory | With Hindsight |
|---|---|
| Generic advice every session | Personalized guidance based on YOUR history |
| You re-explain your skills each time | Agent recalls skills from past conversations |
| Rejections are forgotten | Agent learns from rejections to avoid similar mismatches |
| No career progression tracking | Agent connects dots across weeks of conversations |

## Architecture

```
Student ←→ Chat UI ←→ FastAPI Backend ←→ Groq LLM (reasoning)
                              ↕
                      Hindsight Cloud
                    retain() / recall() / reflect()
```

**Core flow on every message:**
1. `recall()` — Pull relevant memories about this student
2. LLM generates personalized response using memories as context
3. `retain()` — Store new information from the conversation
4. Over time, Hindsight consolidates facts into observations and mental models

## Hindsight Integration Details

We use three Hindsight operations:

- **`retain()`** — After every conversation turn, we store the student's message and our response. Hindsight automatically extracts structured facts (skills, goals, rejections, interests) and builds entity relationships.

- **`recall()`** — Before generating each response, we query Hindsight with the student's message. It runs 4 retrieval strategies in parallel (semantic, keyword, entity graph, temporal) to find the most relevant memories.

- **`reflect()`** — Available via the "Reflect" button. Hindsight synthesizes all stored memories into a comprehensive understanding of the student's career profile, connecting dots that individual recall queries might miss.

## Quick Start

### Prerequisites
- Python 3.10+
- A [Groq](https://groq.com/) API key (free tier)
- A [Hindsight Cloud](https://ui.hindsight.vectorize.io) account (use promo code `MEMHACK315` for $50 free credits)

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/career-advisor.git
cd career-advisor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run
python app.py
```

Open http://localhost:8000 and start chatting!

### Demo Flow (3 sessions)

**Session 1** — Establish the student profile:
- "I know Python and React. I built a web scraper for internship listings."
- "I'm really interested in data science and machine learning."

**Session 2** — Add a rejection:
- "I applied to DataCorp's data analyst role but got rejected."
- "They said I need stronger SQL skills and Tableau experience."

**Session 3** — Watch the agent connect the dots:
- "What should I focus on next?"
- The agent recalls your Python skills, data interest, AND the DataCorp rejection — then proactively suggests SQL learning resources and alternative internships that match your profile.

## Tech Stack

- **Memory**: [Hindsight](https://hindsight.vectorize.io/) by Vectorize — [Agent Memory](https://vectorize.io/features/agent-memory)
- **LLM**: [Groq](https://groq.com/) (qwen/qwen3-32b)
- **Backend**: Python, FastAPI
- **Frontend**: Vanilla HTML/CSS/JS

## Team

- [Your Name] — [Your Role]

## Links

- [Hindsight Documentation](https://hindsight.vectorize.io/)
- [Hindsight GitHub](https://github.com/vectorize-io/hindsight)
- [Agent Memory by Vectorize](https://vectorize.io/features/agent-memory)
