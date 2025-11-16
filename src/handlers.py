"""
Telegram message handlers for audio diary transcription.
"""
import os
import logging
from pathlib import Path
import tempfile
from telegram import Update
from telegram.ext import ContextTypes
from gemini_transcriber import GeminiTranscriber

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when /start is issued."""
    await update.message.reply_text(
        "🎙️ Welcome to Audio Diary Transcriber!\n\n"
        "Send me an audio file and I'll transcribe it to English romanized text.\n"
        "Supported formats: MP3, M4A, WAV, AIFF, OGG, FLAC"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when /help is issued."""
    await update.message.reply_text(
        "📖 How to use:\n\n"
        "1. Send an audio file\n"
        "2. I'll transcribe it to English romanized text\n\n"
        "Commands:\n"
        "/start - Show welcome message\n"
        "/help - Show this help message"
    )


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle audio file transcription."""
    try:
        # Show processing message
        processing_msg = await update.message.reply_text("⏳ Processing your audio...")

        # Download audio file
        file = await update.message.audio.get_file()

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_path = tmp_file.name
            await file.download_to_drive(custom_path=tmp_path)

        try:
            # Transcribe
            api_key = os.getenv("GEMINI_API_KEY")
            transcriber = GeminiTranscriber(api_key=api_key)

            prompt = (
                "This is an audio diary recording in Bengali. "
                "Hindi or English words may be used. "
                "Transcribe this into English romanized fonts. "
                "Only output the transcription and nothing else."
            )

            transcript = transcriber.transcribe(tmp_path, prompt=prompt)

            if transcript:
                # Edit the processing message with result
                await processing_msg.edit_text(f"✅ Transcription:\n\n{transcript}")
            else:
                await processing_msg.edit_text("❌ Failed to transcribe audio. Please try again.")

        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle voice message transcription."""
    try:
        # Show processing message
        processing_msg = await update.message.reply_text("⏳ Processing your voice message...")

        # Download voice file
        file = await update.message.voice.get_file()

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp_file:
            tmp_path = tmp_file.name
            await file.download_to_drive(custom_path=tmp_path)

        try:
            # Transcribe
            api_key = os.getenv("GEMINI_API_KEY")
            transcriber = GeminiTranscriber(api_key=api_key)

            prompt = (
                "This is an audio diary recording in Bengali. "
                "Hindi or English words may be used. "
                "Transcribe this into English romanized fonts. "
                "Only output the transcription and nothing else."
            )

            transcript = transcriber.transcribe(tmp_path, prompt=prompt)

            if transcript:
                # Edit the processing message with result
                await processing_msg.edit_text(f"✅ Transcription:\n\n{transcript}")
            else:
                await processing_msg.edit_text("❌ Failed to transcribe audio. Please try again.")

        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except Exception as e:
        logger.error(f"Error processing voice: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")
