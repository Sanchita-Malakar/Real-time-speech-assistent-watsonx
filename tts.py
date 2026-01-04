import requests
import pygame
import time
import os
from config import TTS_API_KEY, TTS_URL

pygame.mixer.init()

def speak(text):
    """Convert text to speech and play audio"""
    if not text or not text.strip():
        return
    
    print("🔊 Speaking:", text[:100] + "..." if len(text) > 100 else text)

    headers = {
        "Content-Type": "application/json",
        "Accept": "audio/wav"
    }

    auth = ("apikey", TTS_API_KEY)

    params = {
        "voice": "en-US_AllisonV3Voice"
    }

    payload = {
        "text": text
    }

    try:
        # IMPORTANT: Stop and unload any currently playing audio first
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        
        # Small delay to ensure file is released
        time.sleep(0.1)

        response = requests.post(
            TTS_URL,
            headers=headers,
            params=params,
            auth=auth,
            json=payload,
            stream=True,
            timeout=10
        )

        if response.status_code != 200:
            print("❌ TTS Error:", response.text)
            return

        # Use a temporary unique filename to avoid conflicts
        audio_file = "response.wav"
        
        # Remove old file if exists
        if os.path.exists(audio_file):
            try:
                os.remove(audio_file)
            except PermissionError:
                # If locked, try alternative filename
                audio_file = f"response_{int(time.time())}.wav"

        # Save audio file
        with open(audio_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)

        # Play audio
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        # Unload after playing to release the file
        pygame.mixer.music.unload()
        time.sleep(0.1)
        
        # Clean up the audio file
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
        except:
            pass  # Ignore cleanup errors
            
    except requests.Timeout:
        print("❌ TTS request timed out")
    except Exception as e:
        print(f"❌ TTS Error: {e}")