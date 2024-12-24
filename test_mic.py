import pyaudio

def test_mic():
    try:
        # Initialize PyAudio
        p = pyaudio.PyAudio()
        
        # Get the default input device
        default_input = p.get_default_input_device_info()
        print(f"Default input device: {default_input['name']}")
        
        # List all audio devices
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:  # Only show input devices
                print(f"\nInput Device {i}:")
                print(f"Name: {info['name']}")
                print(f"Channels: {info['maxInputChannels']}")
                print(f"Sample Rate: {int(info['defaultSampleRate'])}")
        
        p.terminate()
        print("\nPyAudio test successful!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Check if microphone is properly connected")
        print("2. Check Windows sound settings")
        print("3. Try running as administrator")
        print("4. Verify microphone permissions in Windows Privacy settings")

if __name__ == "__main__":
    test_mic() 