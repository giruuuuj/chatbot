import pyttsx3

def test_tts():
    try:
        engine = pyttsx3.init()
        
        # Print available voices
        voices = engine.getProperty('voices')
        print("Available voices:")
        for voice in voices:
            print(f"Voice ID: {voice.id}")
            print(f"Voice Name: {voice.name}")
            print(f"Voice Languages: {voice.languages}")
            print("---")
        
        # Test speech
        engine.say("Testing text to speech. Can you hear this?")
        engine.runAndWait()
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_tts() 