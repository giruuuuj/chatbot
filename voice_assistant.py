import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
import pyttsx3
import threading
import datetime
import webbrowser
import time

class VoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("600x700")
        self.root.configure(bg='#2C3E50')
        
        # Initialize text-to-speech engine
        try:
            self.engine = pyttsx3.init()
            self.initialize_tts()
        except Exception as e:
            print(f"TTS Error: {str(e)}")
            messagebox.showerror("Error", "Text-to-speech initialization failed!")
        
        # Create UI elements
        self.create_ui()
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        # Welcome message
        self.display_message("Assistant: Hello! How can I help you today?")
        self.speak_text("Hello! How can I help you today?")
    
    def initialize_tts(self):
        """Initialize text-to-speech engine with settings"""
        voices = self.engine.getProperty('voices')
        # Try to set a female voice if available
        for voice in voices:
            if "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
    
    def create_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Voice Assistant",
            font=('Arial', 24, 'bold'),
            bg='#2C3E50',
            fg='white'
        )
        title_label.pack(pady=10)
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=('Arial', 12),
            bg='#34495E',
            fg='white'
        )
        self.chat_area.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready to listen...",
            font=('Arial', 12),
            bg='#2C3E50',
            fg='#2ECC71'
        )
        self.status_label.pack(pady=5)
        
        # Microphone button
        self.mic_button = tk.Button(
            main_frame,
            text="🎤 Click to Speak",
            font=('Arial', 14, 'bold'),
            bg='#3498DB',
            fg='white',
            relief=tk.RAISED,
            command=self.toggle_listening
        )
        self.mic_button.pack(pady=10)
    
    def speak_text(self, text):
        """Speak text using TTS engine"""
        try:
            def speak():
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as e:
                    print(f"Speech Error: {str(e)}")
                finally:
                    self.engine.stop()
            
            speech_thread = threading.Thread(target=speak)
            speech_thread.daemon = True
            speech_thread.start()
            
        except Exception as e:
            print(f"TTS Error: {str(e)}")
            self.status_label.config(text="Speech Error!")
    
    def display_message(self, message):
        """Display message in chat area"""
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.see(tk.END)
    
    def process_command(self, text):
        """Process voice commands"""
        text = text.lower()
        
        if "time" in text:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
        elif "date" in text:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            response = f"Today's date is {current_date}"
        elif "search" in text:
            query = text.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            response = f"Searching for {query}"
        elif any(word in text for word in ["hello", "hi", "hey"]):
            response = "Hello! How can I help you today?"
        elif "help" in text:
            response = """I can help you with:
            - Telling time and date
            - Web searches
            - Answering questions
            - Basic calculations
            Just ask me anything!"""
        elif "bye" in text:
            response = "Goodbye! Have a great day!"
        else:
            response = f"I heard you say: {text}. How can I help with that?"
        
        self.display_message(f"You: {text}")
        self.display_message(f"Assistant: {response}")
        self.speak_text(response)
    
    def toggle_listening(self):
        """Toggle listening state"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start listening for voice input"""
        self.is_listening = True
        self.mic_button.config(
            text="🔴 Listening... Click to Stop",
            bg='#E74C3C'
        )
        self.status_label.config(text="Listening...")
        threading.Thread(target=self.listen_for_speech).start()
    
    def stop_listening(self):
        """Stop listening for voice input"""
        self.is_listening = False
        self.mic_button.config(
            text="🎤 Click to Speak",
            bg='#3498DB'
        )
        self.status_label.config(text="Ready to listen...")
    
    def listen_for_speech(self):
        """Listen for speech input"""
        try:
            with sr.Microphone() as source:
                self.status_label.config(text="Adjusting for noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                while self.is_listening:
                    try:
                        self.status_label.config(text="Listening...")
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        
                        self.status_label.config(text="Processing speech...")
                        text = self.recognizer.recognize_google(audio)
                        
                        self.process_command(text)
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        self.status_label.config(text="Speech not recognized. Please try again.")
                    except sr.RequestError:
                        self.status_label.config(text="Sorry, there was an error with the speech service.")
                        
        except Exception as e:
            self.status_label.config(text="Error with microphone. Please check your settings.")
            messagebox.showerror("Error", f"Microphone Error: {str(e)}")
        
        finally:
            self.stop_listening()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistant(root)
    root.mainloop() 