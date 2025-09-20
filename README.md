# 🤖 AI Charades - Backend

This is the **FastAPI backend** for [AI Charades](#), a game where the player performs actions on webcam and an AI opponent tries to guess in real time.  

The backend receives image frames from the React frontend, sends them to an AI model (e.g., Gemini Vision API), and returns guesses.

[See Frontend](https://github.com/PennApps2025/FrontAiCharades)

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
uvicorn app.main:app --reload


📂 Project Structure
BackAiCharades/
├── main.py              # FastAPI app
├── requirements.txt     # Python dependencies
├── venv/                # Virtual environment (optional, local)
└── ...

📜 License

MIT License © 2025 PennApps2025 Team
