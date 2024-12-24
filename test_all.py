import speech_recognition as sr
import pyttsx3
import pyaudio

def test_all_components():
    print("Testing all components...")
    
    # Test PyAudio
    print("\n1. Testing PyAudio...")
    try:
        p = pyaudio.PyAudio()
        print("PyAudio initialized successfully!")
        device_count = p.get_device_count()
        print(f"Found {device_count} audio devices")
        p.terminate()
    except Exception as e:
        print(f"PyAudio Error: {str(e)}")
    
    # Test Speech Recognition
    print("\n2. Testing Speech Recognition...")
    try:
        recognizer = sr.Recognizer()
        print("Speech Recognition initialized successfully!")
    except Exception as e:
        print(f"Speech Recognition Error: {str(e)}")
    
    # Test Text-to-Speech
    print("\n3. Testing Text-to-Speech...")
    try:
        engine = pyttsx3.init()
        print("Text-to-Speech initialized successfully!")
    except Exception as e:
        print(f"Text-to-Speech Error: {str(e)}")

if __name__ == "__main__":
    test_all_components() 