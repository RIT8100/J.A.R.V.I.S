# save as jarvis_minimal.py
import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import subprocess
from datetime import datetime

# TTS setup
tts = pyttsx3.init()
tts.setProperty("rate", 170)

def say(text):
    print("JARVIS:", text)
    tts.say(text)
    tts.runAndWait()

# STT setup
r = sr.Recognizer()
mic = sr.Microphone()

def listen(timeout=5, phrase_time_limit=8):
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.4)
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return ""

# Simple intent router
def handle_intent(text):
    text = text.lower()
    if not text:
        return "I didn't hear that."
    # greetings
    if any(w in text for w in ("hello","hi","hey")):
        return "Hello! How can I help?"
    if "time" in text:
        return f"The time is {datetime.now().strftime('%I:%M %p')}."
    if "open youtube" in text:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."
    if "search for" in text:
        q = text.split("search for",1)[1].strip()
        webbrowser.open(f"https://www.google.com/search?q={q}")
        return f"Searching for {q}."
    if "shutdown" in text and "computer" in text:
        say("Are you sure you want to shut down? Say yes to confirm.")
        confirm = listen(5,4).lower()
        if "yes" in confirm:
            say("Shutting down now.")
            # Warning: commented out for safety
            # subprocess.run(["shutdown", "/s", "/t", "0"], check=False)
            return "Shutdown command issued (disabled for safety)."
        return "Okay, canceled."
    return "Sorry, I don't know how to do that yet."

def main_loop():
    say("Jarvis at your service. Say a command.")
    while True:
        print("Listening...")
        text = listen()
        print("Heard:", text)
        if text:
            resp = handle_intent(text)
            say(resp)
        time.sleep(0.3)

if __name__ == "__main__":
    main_loop()
