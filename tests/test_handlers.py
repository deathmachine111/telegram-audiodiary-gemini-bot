"""Unit tests for Telegram handlers."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update, Message, Chat, User, Audio, Voice
from src.handlers import start_command, help_command, handle_audio, handle_voice


@pytest.fixture
def mock_update():
    """Create a mock Telegram Update."""
    update = MagicMock(spec=Update)
    update.message = MagicMock(spec=Message)
    update.message.reply_text = AsyncMock()
    update.message.chat_id = 12345
    return update


@pytest.fixture
def mock_context():
    """Create a mock context."""
    return MagicMock()


class TestStartCommand:
    """Test /start command handler."""

    @pytest.mark.asyncio
    async def test_start_command(self, mock_update, mock_context):
        """Test start command sends welcome message."""
        await start_command(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        args = mock_update.message.reply_text.call_args[0]
        assert "Welcome" in args[0]
        assert "Audio Diary" in args[0]


class TestHelpCommand:
    """Test /help command handler."""

    @pytest.mark.asyncio
    async def test_help_command(self, mock_update, mock_context):
        """Test help command sends help message."""
        await help_command(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        args = mock_update.message.reply_text.call_args[0]
        assert "How to use" in args[0]


class TestHandleAudio:
    """Test audio file handler."""

    @pytest.mark.asyncio
    async def test_audio_processing_starts(self, mock_update, mock_context):
        """Test that processing message is shown."""
        mock_update.message.audio = MagicMock(spec=Audio)
        mock_file = MagicMock()
        mock_file.download_to_drive = AsyncMock()
        mock_update.message.audio.get_file = AsyncMock(return_value=mock_file)

        # Mock the transcriber
        with patch("src.handlers.GeminiTranscriber") as mock_transcriber_class:
            mock_transcriber = MagicMock()
            mock_transcriber_class.return_value = mock_transcriber
            mock_transcriber.transcribe.return_value = "Test transcription"

            with patch("os.path.exists", return_value=True):
                with patch("os.remove"):
                    await handle_audio(mock_update, mock_context)

        # Should have called reply_text twice (processing, then result)
        assert mock_update.message.reply_text.call_count >= 1

    @pytest.mark.asyncio
    async def test_audio_transcription_error(self, mock_update, mock_context):
        """Test error handling during transcription."""
        mock_update.message.audio = MagicMock(spec=Audio)
        mock_file = MagicMock()
        mock_file.download_to_drive = AsyncMock(side_effect=Exception("Download failed"))
        mock_update.message.audio.get_file = AsyncMock(return_value=mock_file)

        await handle_audio(mock_update, mock_context)

        # Should have called reply_text with error message
        mock_update.message.reply_text.assert_called()
        args = mock_update.message.reply_text.call_args[0]
        assert "Error" in args[0] or "❌" in args[0]


class TestHandleVoice:
    """Test voice message handler."""

    @pytest.mark.asyncio
    async def test_voice_processing_starts(self, mock_update, mock_context):
        """Test that processing message is shown for voice."""
        mock_update.message.voice = MagicMock(spec=Voice)
        mock_file = MagicMock()
        mock_file.download_to_drive = AsyncMock()
        mock_update.message.voice.get_file = AsyncMock(return_value=mock_file)

        # Mock the transcriber
        with patch("src.handlers.GeminiTranscriber") as mock_transcriber_class:
            mock_transcriber = MagicMock()
            mock_transcriber_class.return_value = mock_transcriber
            mock_transcriber.transcribe.return_value = "Voice transcription"

            with patch("os.path.exists", return_value=True):
                with patch("os.remove"):
                    await handle_voice(mock_update, mock_context)

        # Should have called reply_text at least once
        assert mock_update.message.reply_text.call_count >= 1

    @pytest.mark.asyncio
    async def test_voice_transcription_error(self, mock_update, mock_context):
        """Test error handling during voice transcription."""
        mock_update.message.voice = MagicMock(spec=Voice)
        mock_file = MagicMock()
        mock_file.download_to_drive = AsyncMock(side_effect=Exception("Download failed"))
        mock_update.message.voice.get_file = AsyncMock(return_value=mock_file)

        await handle_voice(mock_update, mock_context)

        # Should have called reply_text with error message
        mock_update.message.reply_text.assert_called()
        args = mock_update.message.reply_text.call_args[0]
        assert "Error" in args[0] or "❌" in args[0]
