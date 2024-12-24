import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
import threading
import time
import pyttsx3

class SmartAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Voice Assistant")
        self.root.geometry("500x600")
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Slower speech rate
        
        # Create chat display
        self.chat_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=45, height=20,
            font=('Arial', 11)
        )
        self.chat_area.pack(padx=10, pady=10)
        
        # Create status label
        self.status_label = tk.Label(
            root, 
            text="Status: Ready", 
            font=('Arial', 10)
        )
        self.status_label.pack(pady=5)
        
        # Create microphone button
        self.mic_button = tk.Button(
            root, 
            text="🎤 Press and Hold to Speak",
            font=('Arial', 12)
        )
        self.mic_button.pack(pady=10)
        self.mic_button.bind('<ButtonPress-1>', self.start_listening)
        self.mic_button.bind('<ButtonRelease-1>', self.stop_listening)
        
        # Initialize speech recognizer with adjusted settings
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 1000  # Lower threshold for better sensitivity
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.3
        self.is_listening = False
        
        # Welcome message
        self.display_message("System: Ready to listen! Press and hold the button to speak.")
        
    def display_message(self, message):
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.see(tk.END)
        
    def speak_text(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.display_message(f"Speech Error: {str(e)}")
            
    def start_listening(self, event):
        self.is_listening = True
        self.mic_button.config(text="🎤 Listening... Release when done")
        self.status_label.config(text="Status: Listening...")
        threading.Thread(target=self.listen_for_speech).start()
        
    def stop_listening(self, event):
        self.is_listening = False
        self.mic_button.config(text="🎤 Press and Hold to Speak")
        self.status_label.config(text="Status: Processing...")
    
    def listen_for_speech(self):
        try:
            with sr.Microphone() as source:
                # Display available microphones
                mics = sr.Microphone.list_microphone_names()
                self.display_message(f"Available microphones: {len(mics)}")
                
                # Adjust for ambient noise
                self.status_label.config(text="Status: Adjusting for noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.status_label.config(text="Status: Listening...")
                
                while self.is_listening:
                    try:
                        # Listen for audio with timeout
                        audio = self.recognizer.listen(
                            source,
                            timeout=1,
                            phrase_time_limit=5
                        )
                        
                        # Try multiple recognition services
                        try:
                            # Try Google first
                            text = self.recognizer.recognize_google(audio)
                        except:
                            # Fallback to other services if available
                            try:
                                text = self.recognizer.recognize_sphinx(audio)
                            except:
                                raise sr.UnknownValueError
                        
                        # Display recognized text
                        self.display_message(f"You said: {text}")
                        
                        # Process the command
                        response = "I heard you say: " + text
                        self.display_message(f"Assistant: {response}")
                        self.speak_text(response)
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        self.display_message("System: Speech not clear. Please speak louder and clearer.")
                    except sr.RequestError as e:
                        self.display_message(f"System Error: {str(e)}")
                        break
                        
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            self.display_message(f"System Error: Could not access microphone. Please check your settings.")
            messagebox.showerror("Error", f"Microphone Error: {str(e)}")
        
        finally:
            self.status_label.config(text="Status: Ready")
            self.is_listening = False
            self.mic_button.config(text="🎤 Press and Hold to Speak")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartAssistant(root)
    root.mainloop() 