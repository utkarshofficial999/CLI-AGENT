# 🤖 AI CLI Agent - Terminal AI Assistant

> **Taking My First Step Towards AI Engineering** 🚀  
> A lightweight, modular, real-time streaming AI CLI Assistant built from scratch in Python.

---

## 🌟 Overview

The **AI CLI Agent** is a terminal-native application designed to explore how modern AI software interacts with Large Language Models (LLMs). Beyond standard API wrappers, this project demonstrates real-time streaming, conversation history persistence, multi-provider abstractions, and rich terminal interfaces.

### 🔄 System Architecture & Data Flow

```
┌──────────────┐     User Input     ┌──────────────────┐    Add Message    ┌───────────────────┐
│              ├───────────────────►│                  ├──────────────────►│                   │
│ Terminal REPL│                    │   CLI Engine     │                   │ History Manager   │
│   (ui.py)    │◄───────────────────┤   (main.py)      │◄──────────────────┤(JSON Persistence) │
└──────────────┘  Streamed Output   └────────┬─────────┘    Context        └───────────────────┘
                                             │ Pass Messages
                                             ▼
                                   ┌──────────────────┐
                                   │ LLM Client       │
                                   │ (Gemini/OpenAI)  │
                                   └──────────────────┘
```

---

## ✨ Features Implemented

- ⚡ **Real-Time Streaming**: Tokens stream directly to stdout as they arrive from the LLM provider for zero perceived latency.
- 🧠 **Context & History Management**: Maintains in-memory session history and automatically persists conversations to `.chat_history.json`.
- 🤖 **Multi-Provider Architecture**: Standardized client layer supporting **Ollama** (offline local LLMs like `llama3.2`), **Groq** (`groq/compound-mini`), **Google Gemini** (`gemini-2.5-flash`), and **OpenAI** (`gpt-4o-mini`).

- 🎨 **Rich Terminal Formatting**: Uses the `rich` library for colorful banners, Markdown rendering, and status logs.
- 🛠️ **Slash Commands**:
  - `/help`: Display all available slash commands.
  - `/clear`: Reset active conversation context.
  - `/history`: View session message history.
  - `/system <prompt>`: View or update system prompt instructions dynamically.
  - `/model`: Display active provider and model information.
  - `/exit` or `/quit`: Save session history and exit cleanly.

---

## 📁 Codebase Structure

| File | Description |
| :--- | :--- |
| **`main.py`** | Primary application entry point & interactive REPL event loop. |
| **`config.py`** | Environment variable management, `.env` file loader, and key validation. |
| **`llm_client.py`** | Unified streaming LLM client abstraction for Google GenAI and OpenAI APIs. |
| **`history_manager.py`** | Handles context window formatting, system prompts, and JSON file persistence. |
| **`ui.py`** | Terminal UI rendering using `rich` (banners, prompts, markdown, status indicators). |
| **`requirements.txt`** | Project dependencies (`google-genai`, `openai`, `python-dotenv`, `rich`). |
| **`.env.example`** | Configuration template for environment variables and API keys. |
| **`.gitignore`** | Excludes virtual environments (`.venv`), API keys (`.env`), and history logs. |
| **`README.md`** | Comprehensive project documentation. |

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone Repository & Setup Virtual Environment

```bash
# Clone repository
git clone https://github.com/utkarshofficial999/CLI-AGENT.git
cd CLI-AGENT

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

Open `.env` in your text editor and add your API key:

```env
# Google Gemini (Primary)
GEMINI_API_KEY=your_actual_gemini_api_key_here

# OpenAI (Optional Alternative)
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 5. Launch the Assistant

```bash
python main.py
```

---

## 💡 Usage Example

```text
🤖 AI CLI Assistant
Your Personal Terminal-based Generative AI Companion

Provider: GEMINI  |  Model: gemini-2.5-flash
Type /help for slash commands or /exit to quit.

You > What is the difference between synchronous and streaming LLM API calls?

AI > Synchronous API calls wait for the entire response to be generated 
before returning data. Streaming calls yield tokens in real time as 
they are computed, significantly reducing user-perceived latency.
```

---

## 🎯 AI Engineering Roadmap

This foundational project is designed to expand into advanced AI Engineering paradigms:

- [ ] **Function / Tool Calling**: Connect Python scripts to execute shell commands, web searches, and system utilities.
- [ ] **RAG System**: Build local vector embedding search over markdown files and PDFs using ChromaDB/FAISS.
- [ ] **Autonomous AI Agents**: Implement multi-step reasoning and self-debugging execution loops.

---

## 📄 License

Distributed under the MIT License. Feel free to fork and adapt for your own learning journey!
