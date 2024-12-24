import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
import threading
import time
import pyttsx3

class PokemonVoiceChatBox:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Voice Chat")
        self.root.geometry("400x500")
        
        # Configure window theme
        self.root.configure(bg='#FF0000')  # Pokémon red
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # Create chat display area with Pokémon styling
        self.chat_area = scrolledtext.ScrolledText(
            root, 
            wrap=tk.WORD, 
            width=40, 
            height=20,
            font=('Arial', 10),
            bg='#FFFFFF',
            fg='#000000'
        )
        self.chat_area.pack(padx=10, pady=10)
        
        # Create status label
        self.status_label = tk.Label(
            root, 
            text="Status: Ready", 
            bg='#FF0000', 
            fg='#FFFFFF',
            font=('Arial', 10, 'bold')
        )
        self.status_label.pack(pady=5)
        
        # Create microphone button with Pokéball styling
        self.mic_button = tk.Button(
            root, 
            text="🎤 Press and Hold to Speak",
            bg='#FFFFFF',
            fg='#000000',
            font=('Arial', 10, 'bold')
        )
        self.mic_button.pack(pady=10)
        self.mic_button.bind('<ButtonPress-1>', self.start_listening)
        self.mic_button.bind('<ButtonRelease-1>', self.stop_listening)
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5
        self.is_listening = False
        self.audio = None
        
        # Welcome message
        self.display_and_speak("Pokémon Assistant: Hello Trainer! How can I help you today?")
        
    def display_and_speak(self, message):
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.see(tk.END)
        # Speak in a separate thread to avoid freezing
        threading.Thread(target=self.speak_text, args=(message,)).start()
        
    def speak_text(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {str(e)}")
            
    def process_command(self, text):
        text = text.lower()
        if "hello" in text or "hi" in text:
            response = "Hello Trainer! Ready for a Pokémon adventure?"
        elif "pokemon" in text:
            response = "I love Pokémon! What's your favorite?"
        elif "pikachu" in text:
            response = "Pika Pika! Pikachu is the most famous Pokémon!"
        elif "bye" in text:
            response = "Goodbye Trainer! Come back soon!"
        else:
            response = "I'm still learning about Pokémon. Can you tell me more?"
            
        self.display_and_speak(f"Pokémon Assistant: {response}")
        
    def start_listening(self, event):
        self.is_listening = True
        self.mic_button.config(text="🔴 Listening... Release when done")
        self.status_label.config(text="Status: Starting...")
        thread = threading.Thread(target=self.listen_for_speech)
        thread.start()
        
    def stop_listening(self, event):
        self.is_listening = False
        self.mic_button.config(text="🎤 Press and Hold to Speak")
        self.status_label.config(text="Status: Processing...")
    
    def listen_for_speech(self):
        try:
            with sr.Microphone() as source:
                self.status_label.config(text="Status: Adjusting for noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                self.status_label.config(text="Status: Listening...")
                
                while self.is_listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        self.chat_area.insert(tk.END, f"Trainer: {text}\n")
                        self.chat_area.see(tk.END)
                        self.process_command(text)
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        self.display_and_speak("System: Speech not recognized. Please try again.")
                    except sr.RequestError as e:
                        self.display_and_speak(f"System Error: {str(e)}")
                        break
                        
        except Exception as e:
            self.status_label.config(text=f"Status: Error - {str(e)}")
            messagebox.showerror("Error", f"Microphone Error: {str(e)}")
        
        finally:
            self.status_label.config(text="Status: Ready")
            self.is_listening = False
            self.mic_button.config(text="🎤 Press and Hold to Speak")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonVoiceChatBox(root)
    root.mainloop() 