# 🤖 AI Charades - Backend

This is the **FastAPI backend** for [AI Charades](#), a game where the player performs actions on webcam and an AI opponent tries to guess in real time.  

The backend receives image frames from the React frontend, sends them to an AI model (e.g., Gemini Vision API), and returns guesses.

---

## 🚀 Tech Stack
- **FastAPI** (Python)
- **Uvicorn** (ASGI server)
- **Pillow / OpenCV** (image handling)
- **google-generativeai** (Gemini Vision API integration)
- **python-multipart** (for file uploads)

---

## ✨ Features
- 📡 `/guess` endpoint for frame uploads  
- 🖼️ Processes images from the frontend  
- 🧠 AI-powered guessing via Gemini Vision API  
- ⚡ Lightweight, async FastAPI server  

---

## ⚡ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/PennApps2025/BackAiCharades.git
cd BackAiCharades

2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run the Server
uvicorn main:app --reload


Backend runs at:
👉 http://localhost:8000

📜 Example Request
curl -X POST "http://localhost:8000/guess" \
  -F "file=@frame.jpg" \
  -F "word=jumping"


Example response:

{
  "guess": "The person looks like they are jumping."
}

🔗 Frontend Connection

The React frontend (repo: FrontAiCharades
) sends images to this backend at:

http://localhost:8000/guess

Make sure both repos are running simultaneously:

Frontend → http://localhost:3000

Backend → http://localhost:8000

📂 Project Structure
BackAiCharades/
├── main.py              # FastAPI app
├── requirements.txt     # Python dependencies
├── venv/                # Virtual environment (optional, local)
└── ...

📜 License

MIT License © 2025 PennApps2025 Team
