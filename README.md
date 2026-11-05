# Local AI Personal Assistant (Jarvis v1)

A fully local, voice-controlled AI assistant written in Python. Everything runs on your own computer: the language model, speech recognition, voice and memory. No cloud service sees your conversations.

> This was my first assistant (July 2025). Its successor is **MIMIR** (*Machine Intelligence for Memory, Insight & Reasoning*), with natural two-way voice, interruption handling, voice ID and long-term memory.

## ✨ Features
- **Local intelligence:** a locally hosted Llama 3 8B (via Ollama) handles the conversation.
- **Voice in, voice out:** push-to-talk recording, OpenAI Whisper for speech-to-text, pyttsx3 for the reply.
- **Push-to-talk privacy:** the microphone is on only while you hold the right Ctrl key.
- **Long-term memory (RAG):** past conversations are stored in a ChromaDB vector database and recalled as context for new questions.
- **Emotion awareness:** TextBlob sentiment analysis tells the model whether you sound positive, negative or neutral.
- **Safe toolbox:** a fixed list of actions the model can trigger: open Spotify, Gmail, YouTube, Google, Calculator, Notepad, Command Prompt or File Explorer.
- **Mood-aware music:** picks a Spotify playlist that matches your detected mood.

## 🛠️ Tech stack
| Part | Tool |
|---|---|
| Language | Python 3.12 |
| LLM | Ollama + Llama 3 8B |
| Speech-to-text | OpenAI Whisper (`base`) |
| Text-to-speech | pyttsx3 (offline Windows voices) |
| Memory | ChromaDB (built-in all-MiniLM-L6-v2 embeddings) |
| Emotion | TextBlob |
| System | PyAudio, keyboard, webbrowser |

## 🚀 Setup (Windows)
1. **Get the code**
   ```bash
   git clone https://github.com/Akhil-7770/Local-AI-Assistant.git
   cd Local-AI-Assistant
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python -m textblob.download_corpora
   ```
2. **Install Ollama** from ollama.com, then pull the model:
   ```bash
   ollama pull llama3:8b
   ```
3. **Install FFmpeg** (Whisper needs it). Either add it to your PATH, or set `FFMPEG_DIR` to the folder that contains `ffmpeg.exe`:
   ```bash
   set FFMPEG_DIR=C:\path\to\ffmpeg\bin
   ```
4. **Optional:** put your own Spotify playlist URIs in `open_spotify()` in `voice_chat.py`.
5. **Run it**
   ```bash
   python voice_chat.py
   ```
   Wait for the models to load, then hold **right Ctrl** and speak. Say "goodbye" to exit.

## ⚠️ Limitations
- **Reasoning:** an 8B model sometimes misreads context or picks the wrong tool.
- **Latency:** transcription plus local inference on consumer hardware means a noticeable pause before each reply.
- **Spotify:** it opens a playlist but can't press play (that would need the Spotify Web API).
- **Windows-only** as written (the `start` commands and pyttsx3 voices).

## 👤 Author
Akhil V ([Akhil-7770](https://github.com/Akhil-7770))

## 📜 License
MIT. See [LICENSE.md](LICENSE.md).
