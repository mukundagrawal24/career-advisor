# CareerPilot - AI Career Advisor That Learns From Every Conversation

> An AI career mentor that remembers your skills, tracks your rejections, analyzes your resume, and gets smarter about your career path over time - powered by [Hindsight](https://github.com/vectorize-io/hindsight) agent memory.

## The Problem

Students struggle to track their evolving skills, internship applications, and career progress. Generic career advice doesn't account for your personal history - your specific skills, what you've been rejected from, and what you're actually interested in. Every AI conversation starts from scratch.

## The Solution

CareerPilot is an AI career advisor with **persistent memory**. It remembers everything across conversations and connects the dots you never asked about.

| Without Memory | With Hindsight |
|---|---|
| Generic advice every session | Personalized guidance based on YOUR history |
| You re-explain your skills each time | Agent recalls skills from past conversations |
| Rejections are forgotten | Agent learns from rejections to avoid similar mismatches |
| No career progression tracking | Agent connects dots across weeks of conversations |

## Features

- **Career Coach** - AI chat with persistent memory across sessions. Remembers your skills, interests, rejections, and goals.
- **Resume Analyzer** - Paste your resume and get detailed feedback on improvements, skill gaps, and matching roles.
- **Student Profile** - Set up your profile on the Dashboard and view it in My Profile. Saved to Hindsight memory.
- **Memory Badges** - Every response shows how many memories were recalled, expandable to see exactly what the agent remembered.
- **Suggested Prompts** - Quick-action chips after each response for faster interaction.
- **Chat History** - All conversations saved in the sidebar for easy access.

## Demo Flow

**Step 1 (Dashboard):** Student fills in profile - name, skills, goals. Saved to Hindsight memory.

**Step 2 (Resume Analyzer):** Student pastes resume. AI gives detailed feedback on improvements, skill gaps, and matching roles.

**Step 3 (Career Coach - Chat 1):** Student says "I know Python and React. What career paths fit?" Agent stores skills and responds with personalized advice.

**Step 4 (Career Coach - Chat 2):** Student says "Got rejected from DataCorp. They said I need SQL." Agent stores the rejection and reason.

**Step 5 (Career Coach - Chat 3):** Student asks "What should I focus on next?" Agent RECALLS Python skills, data interest, AND the DataCorp rejection from previous sessions - then proactively suggests SQL learning resources and alternative internships.

**The magic:** In Chat 3, the agent was never told about Chat 1 or Chat 2. It recalled everything from Hindsight memory and connected the dots on its own.

## Architecture

```
Student (Browser) --> Chat UI (index.html)
                          |
                    POST /api/chat
                          |
                    FastAPI Backend (app.py)
                     /         \
              recall()        retain()
                |                |
          Hindsight Cloud   Hindsight Cloud
          (get memories)    (store new info)
                \               /
                  Groq LLM
               (qwen3-32b)
                     |
              AI Response + Memory Badges
                     |
                  Back to UI
```

**Every message flow:**
1. `recall()` - Pull relevant memories about this student from Hindsight
2. Send message + memories to Groq LLM for personalized reasoning
3. `retain()` - Store new facts from the conversation in Hindsight
4. Response + memory badges sent back to the UI

## Hindsight Integration

We use two core Hindsight operations:

### retain() - Storing Memories
After every conversation turn, we send both the student's message and the AI's response to Hindsight. It automatically extracts structured facts like "student knows Python", "student was rejected from DataCorp", "student interested in data science".

```python
hindsight.retain(
    bank_id="career-advisor",
    content="Student said: I know Python. Advisor responded: Great! ...",
    metadata={"user_id": "student-123"},
)
```

### recall() - Retrieving Memories
Before generating each response, we query Hindsight with the student's current message. It runs 4 retrieval strategies in parallel (semantic search, keyword matching, entity graph traversal, temporal filtering) and returns the most relevant memories.

```python
results = hindsight.recall(
    bank_id="career-advisor",
    query="What should I focus on next?",
    metadata={"user_id": "student-123"},
)
# Returns: Python skills, data science interest, DataCorp rejection...
```

These memories are injected into the LLM prompt as context, enabling the agent to give personalized responses without the student repeating information.

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Memory | [Hindsight Cloud](https://hindsight.vectorize.io/) by Vectorize | Biomimetic memory with 4-way parallel retrieval |
| LLM | [Groq](https://groq.com/) (qwen/qwen3-32b) | Free tier, extremely fast inference |
| Backend | Python + FastAPI | Simple, fast, perfect for prototyping |
| Frontend | HTML + CSS + JS | Single-file UI with sidebar, multiple pages |

## Quick Start

### Prerequisites
- Python 3.10+
- A [Groq](https://groq.com/) API key (free tier)
- A [Hindsight Cloud](https://ui.hindsight.vectorize.io) account (use promo code `MEMHACK315` for $50 free credits)

### Setup

```bash
git clone https://github.com/mukundagrawal24/career-advisor.git
cd career-advisor
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python app.py
```

Open http://localhost:8000 and start chatting!

## Project Files

| File | Purpose |
|------|---------|
| `app.py` | FastAPI backend - handles chat, calls Groq LLM, calls Hindsight for retain/recall |
| `static/index.html` | Full UI - Dashboard, Resume Analyzer, Career Coach, My Profile |
| `.env` | Secret API keys (not on GitHub) |
| `.env.example` | Template for setting up API keys |
| `requirements.txt` | Python dependencies |

## What Makes This Innovative

- Agent **connects dots proactively** (rejection + skills = personalized career path)
- Memory is **transparent** to the user via expandable memory badges
- **Resume analysis** stored in memory and referenced in future conversations
- **Profile system** feeds into Hindsight for richer context
- Multiple pages (Dashboard, Resume, Chat, Profile) all powered by the same memory backend

## Team

- **Mukund Agrawal** - Team Lead, Backend, Integration
- **Siva Sai Prakash Rayudu** - Frontend, UX
- **Muhammad Waseem Rahmani** - Prompt Engineering, Testing
- **Jagana Vaishnavi** - Content, Video, Testing

## Links

- [Hindsight GitHub](https://github.com/vectorize-io/hindsight)
- [Hindsight Documentation](https://hindsight.vectorize.io/)
- [Agent Memory by Vectorize](https://vectorize.io/features/agent-memory)