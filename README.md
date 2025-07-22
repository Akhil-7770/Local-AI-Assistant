Local AI Personal Assistant (Codename: Jarvis)

This project is a fully local, voice-controlled AI personal assistant built in Python. It was designed from the ground up to prioritize user privacy and run entirely on local hardware, without relying on cloud services for its core intelligence, memory, or voice recognition.

The assistant, nicknamed Jarvis, can understand spoken commands, respond with a synthesized voice, learn from conversations, and perform a limited set of safe, pre-defined actions on the user's computer. This project serves as a comprehensive prototype demonstrating the integration of multiple AI and system technologies into a single, functional application.

✨ Features

100% Local Intelligence: Core reasoning is handled by a locally hosted Large Language Model (Ollama with Llama 3 8B), ensuring conversations remain private.

Voice-Controlled Interface: Interact with the AI naturally using your voice.

Push-to-Talk Privacy: The microphone is only active while holding down the right Ctrl key, preventing unintentional listening.

Persistent Memory (RAG): Utilizes a ChromaDB vector database to store and recall information from past conversations, allowing the AI to learn about the user over time.

Emotion Detection: Employs TextBlob for sentiment analysis to detect if the user's tone is positive, negative, or neutral, enabling more empathetic responses.

Action-Oriented Toolbox: Can perform safe, pre-defined actions like opening applications (Spotify, Notepad, Calculator) and websites (Gmail, YouTube).

Mood-Aware Music: Intelligently selects and opens Spotify playlists based on the user's detected emotion.

Customizable Voice: The Text-to-Speech engine can be configured to use different voices.

🛠️ Tech Stack
Programming Language: Python 3.12

LLM Engine: Ollama

Language Model: Llama 3 8B

Speech-to-Text: OpenAI Whisper

Text-to-Speech: pyttsx3 (for local voice) / Edge TTS (for cloud voice)

Memory/RAG: ChromaDB (Vector Database) & Sentence-Transformers (Embeddings)

Emotion Analysis: TextBlob

System Interaction: PyAudio, Keyboard, Webbrowser

System Dependencies: FFmpeg

🚀 Setup and Installation

To run this project on your own machine, follow these steps.

Prerequisites:

    A Windows machine with a dedicated GPU (NVIDIA recommended, 6GB+ VRAM).

    Python 3.12.

    Git.

1. Clone the Repository


#Bash

git clone https://github.com/your-username/Local-AI-Assistant.git
cd Local-AI-Assistant

2. Create a Virtual Environment

#Bash

python -m venv jarvis_env
.\jarvis_env\Scripts\activate

3. Install Python Dependencies

Install all the required Python libraries from the requirements.txt file.

#Bash

pip install -r requirements.txt

After installation, download the necessary corpora for TextBlob:

#Bash

python -m textblob.download_corpora

4. Install Ollama

Download and install Ollama from the official website.

Pull the Llama 3 8B model by running the following command in your terminal:

#Bash

ollama run llama3:8b

5. Install FFmpeg

Whisper requires FFmpeg for audio processing.

Download the FFmpeg essentials build from Gyan.dev.

Unzip the file and place the resulting folder (e.g., ffmpeg-7.0-essentials_build) somewhere on your system.

Important: You must update the FFMPEG PATH FIX line in the voice_chat.py script to point to the bin directory inside your FFmpeg folder.

6. Configure Spotify (Optional)

To use the mood-aware music feature, open voice_chat.py.

Find the open_spotify function and replace the placeholder URIs in the playlists dictionary with your own Spotify Playlist URIs.

7. Run the Assistant

Once all setup is complete, run the main script from your activated virtual environment:

#Bash

python voice_chat.py

Wait for the models to load, then press and hold the right Ctrl key to speak.

⚠️ Limitations

While the project was a success, it operates under a few key limitations:

LLM Reasoning: The local Llama 3 8B model, while powerful, can sometimes misunderstand complex conversational context or fail to select the correct tool, a common issue with models of this scale.

Performance Latency: There is a noticeable delay between speaking and receiving a response due to the processing time required for transcription (Whisper) and LLM inference on consumer hardware.

Spotify Playback: The assistant can only open a Spotify playlist; it cannot automatically press play. Full playback control would require a more complex integration with the Spotify Web API.

💡 A Foundation for Your Own Projects
This project serves as a foundational prototype. It demonstrates how multiple complex AI systems can be integrated into a single, functional application. While it is a complete and successful proof-of-concept, it is intentionally kept simple to highlight the core architecture.

The modular code provides a clear and robust starting point for anyone looking to build their own, more advanced AI assistants. Feel free to fork this repository and use it as a launchpad for your own unique creations.

🙏 Acknowledgments
This project would not have been possible without the incredible open-source tools provided by the community. Special thanks to the teams behind:

Ollama

OpenAI Whisper

ChromaDB

SentenceTransformers

👤 Author
akhil.v - Initial work & Project Lead - Akhil-7770

📜 License
This project is licensed under the MIT License - see the LICENSE.md file for details.