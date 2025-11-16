"""
Gemini API transcriber for audio files.
Core transcription logic extracted from call-records project.
"""
import base64
import os
from typing import Optional
import google.genai as genai


SUPPORTED_FORMATS = {"mp3", "m4a", "wav", "aiff", "ogg", "flac"}

# MIME type mapping for audio formats
MIME_TYPES = {
    "mp3": "audio/mp3",
    "m4a": "audio/aac",
    "wav": "audio/wav",
    "aiff": "audio/aiff",
    "ogg": "audio/ogg",
    "flac": "audio/flac"
}


def is_valid_audio_file(filename: str) -> bool:
    """Check if filename has a supported audio format."""
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    return ext in SUPPORTED_FORMATS


class GeminiTranscriber:
    """Transcribe audio files using Gemini 2.5 Pro API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize transcriber.

        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not provided and not in environment")

        self.client = genai.Client(api_key=self.api_key)

    def transcribe(
        self,
        audio_path: str,
        prompt: str
    ) -> Optional[str]:
        """
        Transcribe audio file with custom prompt.

        Args:
            audio_path: Path to audio file
            prompt: Custom prompt for Gemini

        Returns:
            Transcription text or None if processing fails
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if not is_valid_audio_file(audio_path):
            raise ValueError(f"Unsupported audio format: {audio_path}")

        # Read and encode audio
        with open(audio_path, "rb") as f:
            audio_data = base64.standard_b64encode(f.read()).decode("utf-8")

        # Get MIME type
        ext = audio_path.lower().rsplit(".", 1)[-1]
        mime_type = MIME_TYPES.get(ext, "audio/mp3")

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": audio_data,
                                }
                            },
                        ],
                    }
                ],
            )

            if response and response.text:
                return response.text
            else:
                return None

        except Exception as e:
            raise RuntimeError(f"Error transcribing audio: {e}")
