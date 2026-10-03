"""
DawaaiDost - ElevenLabs Multilingual Voice Synthesis
Converts medicine instructions into warm, natural, soothing speech in Hindi/English.
Supports ElevenLabs API with browser Web Speech API client fallback.
"""

import os
import requests
import logging

logger = logging.getLogger("DawaaiDost-ElevenLabs")

# Warm, empathetic voice ID (default ElevenLabs multilingual voice)
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel (calm, reassuring)

class ElevenLabsVoiceNarrator:
    def __init__(self, api_key: str = None, voice_id: str = DEFAULT_VOICE_ID):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY", "")
        self.voice_id = voice_id
        self.has_key = bool(self.api_key)

    def generate_audio(self, text: str, output_file: str = "output_speech.mp3") -> dict:
        """
        Synthesizes speech using ElevenLabs API.
        If no API key is provided, returns instructions for client-side Web Speech API playback.
        """
        if not self.has_key:
            logger.info("[OFFLINE MODE] No ELEVENLABS_API_KEY. Using browser Web Speech API for playback.")
            return {
                "source": "web_speech_api",
                "text": text,
                "status": "ready_for_browser_tts",
                "audio_url": None
            }

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8
            }
        }

        try:
            response = requests.post(url, json=data, headers=headers, timeout=15)
            if response.status_code == 200:
                with open(output_file, "wb") as f:
                    f.write(response.content)
                logger.info(f"ElevenLabs audio saved to {output_file}")
                return {
                    "source": "elevenlabs",
                    "file_path": output_file,
                    "status": "success",
                    "audio_url": f"/audio/{os.path.basename(output_file)}"
                }
            else:
                logger.warning(f"ElevenLabs API returned {response.status_code}: {response.text}")
                return {"source": "web_speech_api", "text": text, "status": "fallback"}
        except Exception as e:
            logger.error(f"Failed to generate ElevenLabs speech: {e}")
            return {"source": "web_speech_api", "text": text, "status": "fallback"}

if __name__ == "__main__":
    narrator = ElevenLabsVoiceNarrator()
    res = narrator.generate_audio("Dadi, Pantocid DSR nashte se pehle khali pet lena hai.")
    print("TTS Result:", res)
