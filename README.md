# vidyaai-
# 🌟 VidyaAI++ – Multilingual AI Tutoring Platform for Underprivileged Students

**VidyaAI++** is an AI-powered, multilingual tutoring and mentorship platform built specifically to support underprivileged (BPL) government school students. It delivers personalized, engaging, and accessible education through AI-generated lessons, emotion-based learning adaptation, and gamified experiences.

---

## 🚀 Features

### ✅ Personalized Learning
- Generates course modules based on **Class**, **Subject**, and **Learning Style**
- AI-generated subtopics, concepts, examples, and quizzes
- Multilingual content delivery for language inclusivity

### ✅ Interactive AI Chatbot
- Powered by **Gemini AI (Google)** for real-time Q&A
- Responds like a friendly school teacher with simple, clear explanations
- Supports different learning styles (visual, auditory, etc.)

### ✅ Gamified Progress Tracking
- Auto-calculates completion % based on quiz performance
- Tracks progress through module/subtopic completion

### ✅ Offline-Ready Architecture (Planned)
- Optimized for low-bandwidth environments
- Local caching and fallback mechanisms

---

## 🛠️ Tech Stack

| Tech | Role |
|------|------|
| **Python (Flask)** | Backend API and routing |
| **Google Gemini API** | Content & response generation |
| **HTML/CSS/JS** | Frontend with chatbot UI |
| **Bootstrap/Tailwind (optional)** | UI styling |
| **Jinja2** | Dynamic templating for Flask |

---

## 📂 Project Structure

```bash
vidyaai++
│
├── app.py                 # Main Flask app
├── templates/
│   ├── index.html         # Homepage (class/subject input + chatbot)
│   ├── generated.html     # Module generation results
│   ├── subtopic.html      # Subtopic + quiz display
│   └── learn.html         # Full AI-generated lesson page
│
├── static/                # (Optional) CSS, JS, images
├── chat.py (merged)       # Chatbot logic (now part of app.py)
├── README.md              # This file
└── requirements.txt       # Python dependencies
