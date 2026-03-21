# Career Advisor Hackathon - Complete Setup Guide

## Your Tech Stack
- **Memory**: Hindsight Cloud (by Vectorize)
- **LLM**: Groq (free tier, super fast)
- **Backend**: Python + FastAPI
- **Frontend**: Simple HTML/CSS/JS chat interface
- **Database**: Hindsight handles this for you

---

## Step 1: Sign Up for Everything (15 minutes)

### 1A. Hindsight Cloud
1. Go to: https://ui.hindsight.vectorize.io
2. Create an account
3. Go to **Billing** section
4. Enter promo code: `MEMHACK315` (gives you $50 free credits)
5. Create a new **memory bank** called `career-advisor`
6. Set the bank's **mission** to: "Help students track their career journey, skills, projects, internship applications, and rejections to provide personalized career guidance that improves over time."
7. Copy your **API URL** and **API key** from the dashboard

### 1B. Groq
1. Go to: https://groq.com/
2. Sign up for free
3. Go to API Keys → Create new key
4. Copy the key somewhere safe

### 1C. Python Environment
```bash
# Make sure you have Python 3.10+
python3 --version

# Create project folder
mkdir career-advisor && cd career-advisor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn groq hindsight-client python-dotenv
```

---

## Step 2: Create Your .env File

Create a file called `.env` in your project root:

```env
# Hindsight Cloud
HINDSIGHT_API_URL=https://your-instance.hindsight.vectorize.io
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BANK_ID=career-advisor

# Groq LLM
GROQ_API_KEY=gsk_your_groq_api_key
```

**IMPORTANT**: Never commit this file to GitHub! Add `.env` to your `.gitignore`.

---

## Step 3: Run the App

```bash
# Start the backend
python app.py

# Open your browser to:
# http://localhost:8000
```

---

## Step 4: Test the Demo Flow

Run these three conversations in order:

**Conversation 1** (establishes skills):
- "Hi, I'm a CS student. I know Python pretty well and I've been learning React for a few months."
- "I built a web scraper that collects internship listings from LinkedIn."
- "I'm really interested in data science and machine learning."

**Conversation 2** (adds a rejection):
- "I applied to DataCorp for their data analyst internship but got rejected."
- "They said I needed stronger SQL skills and experience with Tableau."
- "I also applied to TechStart but haven't heard back yet."

**Conversation 3** (the magic moment):
- "What should I focus on next?"
- The agent should recall your skills, interests, and the DataCorp rejection, then proactively suggest a SQL learning path and alternative internships that match your Python/data background without requiring the SQL skills you're missing.

---

## Architecture Overview

```
User → Chat UI → FastAPI Backend → Groq (LLM reasoning)
                       ↕
                Hindsight Cloud
              (retain + recall + reflect)
```

Every message flow:
1. User sends message
2. Backend calls `recall()` to get relevant memories
3. Backend sends message + memories to Groq LLM
4. LLM generates response
5. Backend calls `retain()` to store new information
6. Response sent to user

---

## Alternative: Docker Setup (if Cloud doesn't work)

If Hindsight Cloud gives you trouble, run it locally:

```bash
export GROQ_API_KEY=gsk_your_key

docker run --rm -it --pull always -p 8888:8888 -p 9999:9999 \
  -e HINDSIGHT_API_LLM_PROVIDER=groq \
  -e HINDSIGHT_API_LLM_API_KEY=$GROQ_API_KEY \
  -e HINDSIGHT_API_LLM_MODEL=openai/gpt-oss-120b \
  -v $HOME/.hindsight-docker:/home/hindsight/.pg0 \
  ghcr.io/vectorize-io/hindsight:latest
```

Then use `http://localhost:8888` as your HINDSIGHT_API_URL.

---

## Troubleshooting

- **Groq rate limits**: If you hit rate limits, switch model to `qwen/qwen3-32b`
- **Function calling errors**: The hackathon docs warn about this — add try/except around LLM calls
- **Hindsight slow on first retain**: Normal — it's extracting entities and building the knowledge graph
- **Need help?**: Join the Hindsight Community Slack (link in hackathon docs)
