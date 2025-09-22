# 🤖 CharAIdes - Backend

**🏆 Winner — Most Creative Hack at PennApps XXVI**

CharAIdes is a real-time, AI-powered charades experience where a player acts out a word on webcam and an AI (via this backend) tries to guess it. Built for **[PennApps XXVI](https://devpost.com/software/ai-charade)**, the backend focuses on fast image handling, robust AI integration, and reliable scoring/leaderboard APIs.

[See Frontend](https://github.com/PennApps2025/FrontAiCharades)

## 💡 Inspiration
We wanted to blend physical play with modern AI: take classic charades and let an AI act as the judge in real-time. That makes the game playable anywhere — solo, remote with friends, or in group settings without a human judge.

## ✅ What it does
- Receives live webcam frames and a target word, then invokes Gemini Vision to guess the action
- Returns a structured result indicating the model’s guess and whether it matches the target
- Persists per-player scores and exposes a sorted leaderboard
- Performs lightweight image preprocessing (resize/convert to JPEG) for consistent AI input

## 🧩 Backend features
- FastAPI endpoints:
  - POST `/guess` — multipart upload (frame) + target word → AI guess + match result
  - POST `/leaderboard` — submit score (username + score)
  - GET `/leaderboard` — fetch top scores (sorted desc, limited)
- Local SQLite leaderboard with init/reset + seed helpers
- Image normalization via Pillow (thumbnail → JPEG)
- Simple word-list matching and prompt shaping for reliable classification

## 🚀 Tech Stack
- Backend: FastAPI (Python), Uvicorn (ASGI)
- Storage: SQLite (via Python’s sqlite3)
- Imaging: Pillow
- AI: google-generativeai (Gemini Vision)
- Uploads: python-multipart
- Optional: python-dotenv for local env loading

## 🛠 How we built it
- Defined REST endpoints in FastAPI for `/guess` and `/leaderboard`
- Preprocessed images (resize/convert) and called Gemini Vision through google-generativeai
- Parsed AI responses and matched them against a curated word list with case-insensitive checks
- Implemented SQLite persistence + simple seeding for quick local development and testing

## ⚠️ Challenges & fixes
- Debouncing AI API calls — throttled requests to avoid rate limits under rapid frame submissions
- AI guess strictness — refined prompts and post-processing to constrain outputs to curated words
- Image variability — normalized inputs (size/format) to stabilize model responses
- Performance — reduced payload size and ensured minimal per-request preprocessing overhead

## 🏆 Accomplishments
- Seamless generative-AI interpretation of human gestures in near real-time
- Stable, predictable backend API with low-latency image handling
- Reliable leaderboard flow with simple local persistence

## 📚 What we learned
- Real-time vision + AI benefits from careful input normalization and rate control
- Prompt design and post-processing are key for constrained classification tasks
- Small optimizations (throttling, JPEG normalization) meaningfully improve responsiveness

## 🔭 What's next
- Expand the word list with nuanced gestures and actions
- Add multiplayer modes and persistent accounts
- Experiment with multimodal prompts (audio + visual) to enrich AI judgments

## ⚡ Getting Started

1) Clone the repository
```powershell
git clone https://github.com/PennApps2025/BackAiCharades.git
cd BackAiCharades
```

2) Create and activate a virtual environment

Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3) Install dependencies
```powershell
pip install -r requirements.txt
```

4) Create a `.env` file and add your Gemini API key
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

5) Initialize or reset the local leaderboard DB (seeds sample data)
```powershell
python .\app\init_db.py
```
This drops/recreates the `leaderboard` table and inserts sample rows.

6) Run the server
```powershell
uvicorn app.main:app --reload
```
Open http://localhost:8000/docs for interactive API docs.