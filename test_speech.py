import speech_recognition as sr

def list_microphones():
    print("Testing microphone detection...")
    
    try:
        # Get list of all microphones
        mic_list = sr.Microphone.list_microphone_names()
        print("\nFound these microphones:")
        for i, microphone_name in enumerate(mic_list):
            print(f"Microphone {i}: {microphone_name}")
            
        # Test default microphone
        print("\nTesting default microphone...")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Default microphone is working!")
            print(f"Default microphone name: {source.device_info['name']}")
            
    except AttributeError:
        print("ERROR: PyAudio not installed. Please run:")
        print("pip install pyaudio")
    except OSError as e:
        print("ERROR: No microphone detected or microphone access denied")
        print(f"Error details: {str(e)}")
    except Exception as e:
        print(f"ERROR: Unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    list_microphones() 