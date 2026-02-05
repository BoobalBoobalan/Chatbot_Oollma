# Local AI Chatbot (React + FastAPI + Ollama)

A production-ready, full-stack AI chatbot application that runs locally using Ollama. It features a modern React frontend and a robust FastAPI backend.

## 🏗️ System Architecture

```mermaid
graph TD
    User[User] -->|Interacts| Frontend[React Frontend (Vite)]
    Frontend -->|HTTP POST JSON| Backend[FastAPI Backend]
    Backend -->|Model API Call| AI_Model[Ollama (Local LLM)]
    AI_Model -->|Text Response| Backend
    Backend -->|JSON Response| Frontend
    Frontend -->|Updates UI| User
```

**Text-Based Flow:**
`React UI` <--> `FastAPI (Port 8000)` <--> `Ollama (Port 11434)`

---

## 🚀 Prerequisites

1.  **Python 3.8+** installed.
2.  **Node.js & npm** installed.
3.  **Ollama** installed and running.

---

## 🛠️ Setup Instructions

### 1. Setup Ollama (AI Model)
Ensure Ollama is installed from [ollama.com](https://ollama.com).

Open your terminal and run:
```bash
# Pull the model (approx 4GB)
ollama pull llama3

# Start the Ollama server (if not already running)
ollama serve
```

---

### 2. Setup Backend (FastAPI)

Navigate to the `backend` folder:
```bash
cd backend
```

Create a virtual environment (optional but recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the server:
```bash
python main.py
```
*The backend will start at `http://localhost:8000`.*
*Swagger API Docs available at `http://localhost:8000/docs`.*

---

### 3. Setup Frontend (React)

Open a new terminal and navigate to the `frontend` folder:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run the development server:
```bash
npm run dev
```
*The frontend will start at `http://localhost:5173`.*

---

## 📂 Project Structure

```
ai-chatbot/
├── backend/
│   ├── main.py              # API Endpoints & Logic
│   ├── requirements.txt     # Python Dependencies
│   └── .env                 # API Keys & Config
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MessageBubble.jsx  # Chat UI Component
│   │   │   └── ChatInput.jsx      # Input UI Component
│   │   ├── api.js           # Axios API Client
│   │   ├── App.jsx          # Main Logic
│   │   ├── main.jsx         # Entry Point
│   │   └── index.css        # Tailwind Global Styles
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
└── README.md
```

## ✨ Features

-   **Real-time Chat**: Instant responses from local LLMI.
-   **Markdown Support**: AI responses render with Markdown (code blocks, bold text, etc.).
-   **Auto-Scroll**: Chat window automatically scrolls to the newest message.
-   **Loading States**: Visual feedback while the AI is generating a response.
-   **Error Handling**: Graceful error messages if the backend or Ollama is down.
-   **Clean UI**: Specific styles for User (Blue) and AI (Gray/White).

## 🔮 Future Improvements

1.  **Chat History Persistence**: Store chats in a database (SQLite/PostgreSQL) implemented in FastAPI.
2.  **Streaming Responses**: Use Server-Sent Events (SSE) or WebSockets to stream the AI response token-by-token for a "typing" effect.
3.  **Model Switching**: Add a dropdown in the UI to switch between `llama3`, `mistral`, or `gpt-4` (via OpenAI).
4.  **File Uploads**: Implement RAG (Retrieval Augmented Generation) to chat with PDF/Text files.
5.  **Dark Mode**: Add a toggle for dark mode support in Tailwind.

---

**Developed with ❤️ by Antigravity**
