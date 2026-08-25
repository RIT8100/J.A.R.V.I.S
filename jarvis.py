# save as jarvis_minimal.py
import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import subprocess
from datetime import datetime
import pygame
import os
# TTS setup
tts = pyttsx3.init()
tts.setProperty("rate", 170)

# setting awake word command______----->>>>

def wake_word():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("⏳ Say 'hello jarvis' to activate...")
        r.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                print("🎤 Listening...")
                audio = r.listen(source)
                trigger = r.recognize_google(audio).lower()
                print(f"👂 Heard: {trigger}")

                wake_phrases = ["hello jarvis", "hello zarvis", "hi jarvis", "wake up jarvis", "jarvis", "wake up","hello"]

                if any(phrase in trigger for phrase in wake_phrases):
                    print("✅ Wake word detected!")

                    # 🔊 Play boot-up sound
                    # print(os.path.abspath("bootup.mp3"))
                    # print(os.path.exists("bootup.mp3"))
                    pygame.mixer.init()
                    pygame.mixer.music.load("bootup.mp3")
                    pygame.mixer.music.play()

                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)

                    # speak("At your service sir, what can I do for you?")
                    return
            except sr.UnknownValueError:
                print("🔇 Didn't catch that.")
            except sr.RequestError as e:
                print(f"❗ Google Speech error: {e}")


def say(text):
    print("JARVIS:", text)
    tts.say(text)
    tts.runAndWait()

# STT setup
r = sr.Recognizer()
mic = sr.Microphone()

def listen(timeout=5, phrase_time_limit=10):
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
    # if "play" in text:
    #     song = text.replace("play", "").strip()
    #     play_song_on_youtube(song)
        
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

# def play_song_on_youtube(song_name):
#     print(f"Playing '{song_name}' on YouTube...")
#     pywhatkit.playonyt(song_name)




        

if __name__ == "__main__":
    while True:
        wake_word()
        main_loop()
