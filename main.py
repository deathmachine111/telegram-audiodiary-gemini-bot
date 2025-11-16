"""
Telegram Audio Diary Transcription Bot
Usage: python main.py
"""
import os
import logging
import sys
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from src.handlers import (
    start_command,
    help_command,
    handle_audio,
    handle_voice,
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    # Load environment variables
    load_dotenv()

    # Get credentials
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not telegram_token:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env")
        sys.exit(1)

    if not gemini_key:
        print("Error: GEMINI_API_KEY not found in .env")
        sys.exit(1)

    # Create application
    app = Application.builder().token(telegram_token).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # Message handlers for audio
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # Start bot
    print("🤖 Bot started! Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
