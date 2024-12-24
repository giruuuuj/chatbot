import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import speech_recognition as sr
import threading

class SmartChatAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Chat Assistant")
        self.root.geometry("600x700")
        self.root.configure(bg='#2C3E50')
        
        # Initialize text-to-speech with enhanced settings
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('rate', 150)     # Speed of speech
            self.engine.setProperty('volume', 1.0)   # Max volume (0.0 to 1.0)
            
            # Set voice to first available voice (usually better quality)
            if voices:
                self.engine.setProperty('voice', voices[0].id)
        except Exception as e:
            print(f"TTS initialization error: {str(e)}")
            self.engine = None
        
        # Create main frame to match layout
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Add title label
        title_label = tk.Label(
            main_frame,
            text="Smart Chat Assistant",
            font=('Arial', 24, 'bold'),
            bg='#2C3E50',
            fg='white'
        )
        title_label.pack(pady=10)
        
        # Update chat area styling
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
        
        # Update status label styling
        self.status_label = tk.Label(
            main_frame,
            text="Ready to listen...",
            font=('Arial', 12),
            bg='#2C3E50',
            fg='#2ECC71'
        )
        self.status_label.pack(pady=5)
        
        # Update button styling
        self.speak_button = tk.Button(
            main_frame,
            text="🎤 Click to Speak",
            font=('Arial', 14, 'bold'),
            bg='#3498DB',
            fg='white',
            relief=tk.RAISED,
            command=self.start_listening
        )
        self.speak_button.pack(pady=10)
        
        # Initialize speech recognizer with optimized settings
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 2500      # Lower threshold for better detection
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8        # Shorter pause for more natural speech
        self.recognizer.operation_timeout = 30       # Longer operation timeout
        
        # Add microphone setup
        try:
            self.mic = sr.Microphone()
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
        except Exception as e:
            print(f"Microphone initialization error: {str(e)}")
            self.mic = None
        
        # Flag to track TTS state
        self.is_speaking = False
        
        # Welcome message
        self.say_message("Hello! I'm your smart assistant. How can I help you today?")
    
    def say_message(self, message):
        """Display and speak a message with error handling"""
        self.chat_area.insert(tk.END, f"Assistant: {message}\n")
        self.chat_area.see(tk.END)
        
        if self.engine is not None:
            try:
                threading.Thread(target=self.speak_text, args=(message,), daemon=True).start()
            except Exception as e:
                print(f"TTS Error: {str(e)}")
                # Fallback to just displaying the message
        
    def speak_text(self, text):
        """Speak text using TTS engine with enhanced settings"""
        if self.is_speaking:
            return
            
        try:
            self.is_speaking = True
            # Break long text into sentences for better speech
            sentences = text.split('.')
            for sentence in sentences:
                if sentence.strip():
                    self.engine.say(sentence.strip())
                    self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {str(e)}")
        finally:
            self.is_speaking = False
            
    def process_command(self, text):
        """Process user input and return appropriate response"""
        text = text.lower().strip()
        
        # Dictionary of responses for different queries
        responses = {
            'hello': "Hello! I'm here to help. What would you like to know?",
            'hi': "Hi there! Feel free to ask me any question!",
            'how are you': "I'm doing great and ready to help you! What's on your mind?",
            'what is your name': "I'm your Smart Assistant, ready to help with your questions!",
            'goodbye': "Goodbye! Have a great day!",
            'bye': "Bye! Feel free to come back if you have more questions!",
            'thank you': "You're welcome! Is there anything else you'd like to know?",
            'thanks': "You're welcome! Feel free to ask more questions!",
            'what can you do': """I can help you with several things:
1. Answer general knowledge questions
2. Provide information on various topics
3. Have conversations
4. Tell jokes and fun facts
5. Help with basic queries

Just ask me anything you'd like to know!""",
            'help': "Just ask me any question, and I'll do my best to help you! For example, try asking 'What is Python?' or 'Tell me about space'",
        }
        
        # Check for specific question patterns
        if text.startswith(('what', 'who', 'how', 'why', 'when', 'where')):
            try:
                # Remove question words to get the search term
                search_terms = text.replace('what is', '')\
                                 .replace('who is', '')\
                                 .replace('tell me about', '')\
                                 .strip()
                
                if search_terms:
                    try:
                        import wikipedia
                        wiki_summary = wikipedia.summary(search_terms, sentences=2)
                        return f"Here's what I found: {wiki_summary}\nWould you like to know more?"
                    except:
                        return f"I understand you're asking about {search_terms}. Could you please be more specific?"
            except Exception as e:
                print(f"Search error: {str(e)}")
        
        # Check for matching responses in the dictionary
        for key in responses:
            if key in text:
                return responses[key]
        
        # Default response for unrecognized input
        return f"I heard you say: {text}. You can ask me any question, and I'll try my best to help!"
        
    def start_listening(self):
        """Start the listening process with error checking"""
        if not self.mic:
            self.say_message("Error: Microphone not found. Please check your microphone connection.")
            return
            
        if not self.speak_button['state'] == 'disabled':
            self.speak_button.config(
                text="🎤 Listening...",
                bg='#FF4444',
                state='disabled'
            )
            self.status_label.config(text="Status: Listening...")
            threading.Thread(target=self.listen_and_respond, daemon=True).start()
        
    def listen_and_respond(self):
        """Listen for user input with enhanced error handling"""
        if not self.mic:
            return
            
        try:
            with self.mic as source:
                # Adjust for ambient noise before each listening session
                self.status_label.config(text="Status: Adjusting for background noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                self.status_label.config(text="Status: Listening... (Speak now)")
                audio = self.recognizer.listen(
                    source,
                    phrase_time_limit=10
                )
                
                self.status_label.config(text="Status: Processing speech...")
                
                # Remove timeout parameter from recognize_google
                text = self.recognizer.recognize_google(audio)
                
                if not text:
                    raise sr.UnknownValueError()
                
                # Display user's message
                self.chat_area.insert(tk.END, f"You: {text}\n")
                self.chat_area.see(tk.END)
                
                # Get and speak response
                response = self.process_command(text)
                self.say_message(response)
                    
        except sr.UnknownValueError:
            self.say_message("I couldn't understand that. Please speak clearly and try again.")
            print("Error: Speech not recognized")
            
        except sr.RequestError as e:
            error_msg = "Network error. Please check your internet connection."
            self.say_message(error_msg)
            print(f"Request Error: {str(e)}")
            
        except sr.WaitTimeoutError:
            self.say_message("No speech detected. Please try again.")
            print("Error: Listening timeout")
            
        except Exception as e:
            self.say_message("A technical error occurred. Please try again.")
            print(f"Unexpected Error: {str(e)}")
        
        finally:
            # Reset UI state
            self.speak_button.config(
                text="🎤 Click to Speak",
                bg='#3498DB',
                state='normal'
            )
            self.status_label.config(text="Status: Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartChatAssistant(root)
    root.mainloop() 