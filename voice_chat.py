import pyaudio
import wave
import requests
import json
import whisper
import os
import pyttsx3
import chromadb
import uuid
from textblob import TextBlob
import keyboard
import webbrowser

# --- FFMPEG (needed by Whisper) ---
# If ffmpeg isn't on your PATH, set FFMPEG_DIR to the folder that contains ffmpeg.exe
if os.environ.get("FFMPEG_DIR"):
    os.environ['PATH'] = os.environ["FFMPEG_DIR"] + os.pathsep + os.environ['PATH']

# --- Configuration ---
RATE = 44100
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
WAVE_OUTPUT_FILENAME = "temp_recording.wav"
PUSH_TO_TALK_KEY = "right ctrl"

# --- AI TOOLBOX DEFINITION ---
def open_spotify(emotion="neutral"):
    speak(f"Since you're feeling {emotion}, I'll play some music for you.")
    playlists = { "positive": "spotify:playlist:37i9dQZF1DXdPec7aJc1u6", "negative": "spotify:playlist:37i9dQZF1DX3rxVfibe1L0", "neutral": "spotify:playlist:37i9dQZEVXbNG2KDcFcKOF" }
    uri_to_play = playlists.get(emotion, playlists["neutral"])
    os.system(f"start {uri_to_play}")
    return "I've started a playlist for you on Spotify."
def open_gmail():
    speak("Opening Gmail."); webbrowser.open('https://mail.google.com'); return "I've opened Gmail in your browser."
def open_youtube():
    speak("Opening YouTube."); webbrowser.open('https://www.youtube.com'); return "I've opened YouTube for you."
def open_calculator():
    speak("Opening the calculator."); os.system("start calc"); return "Here is the calculator."
def open_notepad():
    speak("Opening Notepad."); os.system("start notepad"); return "Notepad is open."
def open_cmd():
    speak("Opening Command Prompt."); os.system("start cmd"); return "A new terminal is ready."
def open_explorer():
    speak("Opening File Explorer."); os.system("start explorer"); return "File Explorer is open."
def open_google():
    speak("Opening Google."); webbrowser.open('https://www.google.com'); return "Google is ready for your search."
available_tools = { "open_spotify": open_spotify, "open_gmail": open_gmail, "open_youtube": open_youtube, "open_calculator": open_calculator, "open_notepad": open_notepad, "open_cmd": open_cmd, "open_explorer": open_explorer, "open_google": open_google, }

# --- Load Models ---
print("Loading all AI models. This may take a moment...")
whisper_model = whisper.load_model("base")
print("All models loaded.")
# Memory: ChromaDB embeds text with its built-in all-MiniLM-L6-v2 model
client = chromadb.PersistentClient(path="./memory_db") 
collection = client.get_or_create_collection(name="memory")
def record_audio_ptt():
    print(f"--- Press and hold the '{PUSH_TO_TALK_KEY}' key to speak ---")
    keyboard.wait(PUSH_TO_TALK_KEY)
    # Open the mic only while the key is held (avoids a buffer overflow while waiting)
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Listening...")
    frames = []
    while keyboard.is_pressed(PUSH_TO_TALK_KEY):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    print("Recording finished.")
    stream.stop_stream(); stream.close(); p.terminate()
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS); wf.setsampwidth(p.get_sample_size(FORMAT)); wf.setframerate(RATE); wf.writeframes(b''.join(frames))
def speak(text):
    try:
        engine = pyttsx3.init(); engine.say(text); engine.runAndWait()
    except Exception as e:
        print(f"pyttsx-error: {e}")
def chat_with_ollama(prompt):
    url = 'http://127.0.0.1:11434/api/generate'
    data = {"model": "llama3:8b", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.RequestException as e:
        return f"Error: Could not connect to Ollama. Details: {e}"
def save_memory(text_chunk):
    collection.add(documents=[text_chunk], ids=[str(uuid.uuid4())])
def recall_memories(text_query, n_results=2):
    if collection.count() == 0: return ""
    results = collection.query(query_texts=[text_query], n_results=n_results)
    return " ".join(results['documents'][0])
def analyze_emotion(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.1: return "positive"
    elif analysis.sentiment.polarity < -0.1: return "negative"
    else: return "neutral"

# --- Main Program Loop ---
if __name__ == "__main__":
    print("\nAI Assistant Initialized. Ready for your command.")
    while True:
        record_audio_ptt()
        
        result = whisper_model.transcribe(WAVE_OUTPUT_FILENAME, fp16=False)
        user_text = result['text'].strip()
        
        if not user_text:
            print("No speech detected."); continue

        print(f"Heard: {user_text}")

        if "goodbye" in user_text.lower():
            print("AI: Goodbye."); speak("Goodbye."); break
        
        emotion = analyze_emotion(user_text)
        print(f"[Detected Emotion: {emotion}]")
        
        context = recall_memories(user_text)
        
        # --- FINAL, SMARTEST PROMPT ---
        tool_list = ", ".join(available_tools.keys())
        system_prompt = (
            f"You are Jarvis, a friendly AI companion. You have a toolbox with these tools: [{tool_list}]. "
            "Your primary task is to determine the user's intent. "
            "**If the user is asking for a specific action that matches a tool (like 'open', 'launch', 'show me'), your ONLY response must be 'TOOL_CALL: <tool_name>'.** "
            "**If the user gives a confirmation (like 'yes', 'okay', 'do it') or delegates the choice to you (like 'you choose'), assume they want to use the tool you just suggested.** "
            "**If the user is just talking, expressing a feeling, or asking a question, you must NOT use a tool.** Instead, respond as a friendly and empathetic companion. "
        )
        # -----------------------------
        
        augmented_prompt = f"{system_prompt}\n\nRelevant past context: '{context}'.\nThe user's current emotion is {emotion}. Respond to the user's statement: {user_text}"
        
        ai_response_text = chat_with_ollama(augmented_prompt)
        
        if ai_response_text.startswith("TOOL_CALL:"):
            tool_name = ai_response_text.split("TOOL_CALL:")[1].strip()
            if tool_name in available_tools:
                if tool_name == "open_spotify":
                    confirmation_message = available_tools[tool_name](emotion)
                else:
                    confirmation_message = available_tools[tool_name]()
                
                print(f"AI says: {confirmation_message}")
                save_memory(f"User asked to {tool_name}, and I performed the action.")
            else:
                error_message = f"I tried to use a tool called '{tool_name}', but it's not in my toolbox."
                print(f"AI says: {error_message}")
                speak(error_message)
        else:
            print(f"AI says: {ai_response_text}")
            speak(ai_response_text)
            save_memory(user_text)
            save_memory(ai_response_text)