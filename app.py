"""
CareerPilot - AI Career Advisor with Hindsight Memory
Hackathon Project: AI Agents That Learn Using Hindsight
"""

import os
import re
import json
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_URL = os.getenv("HINDSIGHT_API_URL", "http://localhost:8888")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "career-advisor")
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3-32b")

from groq import Groq
from hindsight_client import Hindsight

groq_client = Groq(api_key=GROQ_API_KEY)

hindsight_kwargs = {"base_url": HINDSIGHT_API_URL}
if HINDSIGHT_API_KEY:
    hindsight_kwargs["api_key"] = HINDSIGHT_API_KEY

hindsight = Hindsight(**hindsight_kwargs)

app = FastAPI(title="CareerPilot")

static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

SYSTEM_PROMPT = """You are CareerPilot, an AI career advisor for students. You help with:
- Tracking skills, projects, and learning progress
- Analyzing internship applications and rejections
- Identifying skill gaps and recommending learning paths
- Suggesting internship opportunities that match the student's profile
- Providing resume and interview tips
- Analyzing resumes and giving detailed feedback

CRITICAL RULES:
1. You have access to MEMORIES from past conversations with this student.
   USE THEM. Reference specific things you remember. This is your superpower.
2. When you recall past information, mention it naturally:
   "I remember you mentioned..." or "Last time we talked, you said..."
3. If you notice skill gaps based on rejections, PROACTIVELY suggest fixes.
4. Be encouraging but honest. If they're missing skills, tell them clearly.
5. Connect the dots between different conversations.
6. Keep responses concise and actionable. Students are busy.
7. When appropriate, suggest specific next steps (courses, projects, applications).
8. When analyzing a resume, give specific, actionable feedback with examples.

PERSONALITY:
- Friendly, like a senior student who's been through it all
- Direct and practical, not fluffy
- Celebrates wins, helps process rejections constructively
"""


def build_prompt_with_memories(user_message, memories):
    if not memories:
        return user_message
    memory_block = "\n".join(f"- {m.text}" for m in memories)
    return f"""RELEVANT MEMORIES FROM PAST CONVERSATIONS:
{memory_block}

---
CURRENT MESSAGE FROM STUDENT:
{user_message}

Use the memories above to give a personalized, context-aware response.
If memories are relevant, reference them naturally in your response."""


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_path = static_dir / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Place index.html in /static folder</h1>")


@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message", "")
    user_id = body.get("user_id", "default-student")
    session_id = body.get("session_id", "session-1")

    if not user_message.strip():
        return JSONResponse({"error": "Empty message"}, status_code=400)

    # Step 1: RECALL memories
    memories = []
    memory_debug = []
    try:
        recall_result = hindsight.recall(
            bank_id=HINDSIGHT_BANK_ID,
            query=user_message,
            metadata={"user_id": user_id},
        )
        memories = recall_result.results if recall_result and recall_result.results else []
        memory_debug = [
            {"text": m.text, "score": getattr(m, "score", None)}
            for m in memories
        ]
    except Exception as e:
        print(f"[WARN] Recall failed: {e}")

    # Step 2: Send to LLM with memories
    enriched_message = build_prompt_with_memories(user_message, memories)

    try:
        llm_response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": enriched_message},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        assistant_reply = llm_response.choices[0].message.content
        assistant_reply = re.sub(r'<think>.*?</think>', '', assistant_reply, flags=re.DOTALL).strip()
    except Exception as e:
        print(f"[ERROR] LLM failed: {e}")
        try:
            llm_response = groq_client.chat.completions.create(
                model="qwen/qwen3-32b",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": enriched_message},
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            assistant_reply = llm_response.choices[0].message.content
            assistant_reply = re.sub(r'<think>.*?</think>', '', assistant_reply, flags=re.DOTALL).strip()
        except Exception as e2:
            return JSONResponse({"error": f"LLM failed: {str(e2)}"}, status_code=500)

    # Step 3: RETAIN in Hindsight
    retain_content = f"Student said: {user_message}\nCareer Advisor responded: {assistant_reply}"
    try:
        hindsight.retain(
            bank_id=HINDSIGHT_BANK_ID,
            content=retain_content,
            context=f"Career advising session. Session: {session_id}",
            metadata={"user_id": user_id, "session_id": session_id},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as e:
        print(f"[WARN] Retain failed: {e}")

    return JSONResponse({
        "reply": assistant_reply,
        "memories_used": len(memory_debug),
        "memories": memory_debug,
        "session_id": session_id,
    })


@app.get("/api/health")
async def health():
    return {"status": "ok", "bank_id": HINDSIGHT_BANK_ID}


if __name__ == "__main__":
    import uvicorn
    print("\n Career Advisor starting up...")
    print(f"   Hindsight: {HINDSIGHT_API_URL}")
    print(f"   Bank: {HINDSIGHT_BANK_ID}")
    print(f"   Model: {GROQ_MODEL}")
    print(f"   Open http://localhost:8000 in your browser\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)