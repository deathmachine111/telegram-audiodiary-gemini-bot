"""Unit tests for GeminiTranscriber."""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from gemini_transcriber import GeminiTranscriber, is_valid_audio_file


class TestIsValidAudioFile:
    """Test audio format validation."""

    def test_valid_formats(self):
        """Test that valid formats are recognized."""
        valid_files = ["audio.mp3", "song.m4a", "record.wav", "file.aiff", "track.ogg", "voice.flac"]
        for filename in valid_files:
            assert is_valid_audio_file(filename) is True

    def test_invalid_formats(self):
        """Test that invalid formats are rejected."""
        invalid_files = ["document.pdf", "image.jpg", "video.mp4", "text.txt"]
        for filename in invalid_files:
            assert is_valid_audio_file(filename) is False

    def test_case_insensitive(self):
        """Test that validation is case insensitive."""
        assert is_valid_audio_file("AUDIO.MP3") is True
        assert is_valid_audio_file("Song.M4A") is True

    def test_no_extension(self):
        """Test files without extension."""
        assert is_valid_audio_file("noextension") is False


class TestGeminiTranscriber:
    """Test GeminiTranscriber class."""

    def test_init_with_api_key(self):
        """Test initialization with explicit API key."""
        transcriber = GeminiTranscriber(api_key="test_key")
        assert transcriber.api_key == "test_key"

    def test_init_without_api_key_raises_error(self):
        """Test initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                GeminiTranscriber()

    @patch.dict(os.environ, {"GEMINI_API_KEY": "env_key"})
    def test_init_from_env(self):
        """Test initialization from environment variable."""
        transcriber = GeminiTranscriber()
        assert transcriber.api_key == "env_key"

    def test_transcribe_file_not_found(self):
        """Test transcription with non-existent file."""
        transcriber = GeminiTranscriber(api_key="test_key")
        with pytest.raises(FileNotFoundError):
            transcriber.transcribe("/nonexistent/file.mp3", prompt="Test prompt")

    def test_transcribe_invalid_format(self, tmp_path):
        """Test transcription with invalid audio format."""
        transcriber = GeminiTranscriber(api_key="test_key")

        # Create a fake text file
        invalid_file = tmp_path / "test.txt"
        invalid_file.write_text("not audio")

        with pytest.raises(ValueError, match="Unsupported audio format"):
            transcriber.transcribe(str(invalid_file), prompt="Test prompt")

    @patch("gemini_transcriber.transcriber.genai.Client")
    def test_transcribe_success(self, mock_client_class, tmp_path):
        """Test successful transcription."""
        # Setup mock
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.text = "Transcribed text"
        mock_client.models.generate_content.return_value = mock_response

        # Create fake audio file
        audio_file = tmp_path / "test.mp3"
        audio_file.write_bytes(b"fake audio data")

        # Test
        transcriber = GeminiTranscriber(api_key="test_key")
        result = transcriber.transcribe(str(audio_file), prompt="Test prompt")

        assert result == "Transcribed text"
        mock_client.models.generate_content.assert_called_once()

    @patch("gemini_transcriber.transcriber.genai.Client")
    def test_transcribe_api_error(self, mock_client_class, tmp_path):
        """Test transcription with API error."""
        # Setup mock to raise error
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.models.generate_content.side_effect = Exception("API Error")

        # Create fake audio file
        audio_file = tmp_path / "test.mp3"
        audio_file.write_bytes(b"fake audio data")

        # Test
        transcriber = GeminiTranscriber(api_key="test_key")
        with pytest.raises(RuntimeError, match="Error transcribing audio"):
            transcriber.transcribe(str(audio_file), prompt="Test prompt")

    @patch("gemini_transcriber.transcriber.genai.Client")
    def test_transcribe_none_response(self, mock_client_class, tmp_path):
        """Test transcription with None response."""
        # Setup mock
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = None
        mock_client.models.generate_content.return_value = mock_response

        # Create fake audio file
        audio_file = tmp_path / "test.mp3"
        audio_file.write_bytes(b"fake audio data")

        # Test
        transcriber = GeminiTranscriber(api_key="test_key")
        result = transcriber.transcribe(str(audio_file), prompt="Test prompt")

        assert result is None
