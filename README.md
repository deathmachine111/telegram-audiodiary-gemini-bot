# 🎙️ Telegram Audio Diary Transcription Bot

Convert your Bengali audio diary entries to English romanized text automatically!

**Features:**
- 📱 Send audio files or voice messages to Telegram
- 🤖 Automatically transcribe to English romanized text using Gemini 2.5 Pro
- 🌍 Supports Bengali, Hindi, and English mixed audio
- ⚡ Fast, reliable, and free to use
- 🧪 Fully tested with pytest
- 🚀 Ready to deploy

## Quick Start

### Local Testing

```bash
# Clone/setup
git clone <repo>
cd telegram-diary-bot
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your credentials

# Run tests
pytest tests/ -v

# Start bot
python main.py
```

### Deployment

Choose one:

- **[PythonAnywhere](DEPLOY_PYTHONANYWHERE.md)** - Easiest, free, good for testing
- **[AWS Lambda](DEPLOY_AWS_LAMBDA.md)** - Serverless, very cheap, fast webhooks
- **[Comparison Guide](DEPLOYMENT_GUIDE.md)** - Help choosing the right platform

## Architecture

### Project Structure
```
telegram-diary-bot/
├── src/
│   ├── __init__.py
│   └── handlers.py          # Telegram message handlers
├── tests/
│   ├── __init__.py
│   └── test_handlers.py     # Unit tests for handlers
├── main.py                  # Bot entry point
├── .env                     # Credentials (not in git)
├── requirements.txt         # Python dependencies
└── DEPLOYMENT_GUIDE.md      # How to deploy
```

### Dependencies Structure
```
telegram-diary-bot → gemini-transcriber
                   ↓
              google-genai (Gemini 2.5 Pro)
```

## Credentials

### Get Your Tokens

1. **Telegram Bot Token**
   - Chat with [@BotFather](https://t.me/botfather) on Telegram
   - /newbot → follow prompts
   - Copy the token

2. **Gemini API Key**
   - Go to https://ai.google.dev/
   - Click "Get API Key"
   - Create new API key in Google Cloud Console

### Setup .env
```bash
cp .env.example .env
# Edit with your values
nano .env
```

## Usage

### For Users
Send your bot an audio file or voice message. It will reply with the transcription in English romanized text.

**Supported formats:** MP3, M4A, WAV, AIFF, OGG, FLAC

### For Developers

#### Add Custom Handlers
Edit `src/handlers.py`:
```python
async def my_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Your custom handler."""
    await update.message.reply_text("Hello!")

# In main.py:
app.add_handler(CommandHandler("mycommand", my_handler))
```

#### Change Transcription Prompt
Edit the prompt in `src/handlers.py`:
```python
prompt = (
    "Custom instruction here. "
    "This audio is in [language]. "
    "Output format: [what you want]."
)
```

#### Use Transcriber Library Elsewhere
```python
from gemini_transcriber import GeminiTranscriber

transcriber = GeminiTranscriber(api_key="YOUR_KEY")
text = transcriber.transcribe(
    audio_path="audio.mp3",
    prompt="Transcribe this audio"
)
print(text)
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src

# Run specific test
pytest tests/test_handlers.py::TestStartCommand -v
```

**Test Results:**
- ✅ 12 transcriber tests (all passing)
- ✅ 6 bot handler tests (all passing)

## Troubleshooting

### Bot doesn't respond
1. Check `.env` has correct tokens
2. Check logs: `python main.py` should show connection
3. Send `/start` command first
4. Check Telegram bot settings in BotFather

### Transcription is wrong
1. Ensure audio quality is good (not too quiet/noisy)
2. Try clearer speech
3. Increase Gemini model (currently using 2.5 Pro)
4. Customize the prompt for your use case

### Deployment issues
- PythonAnywhere: Check Web > Error logs
- AWS Lambda: Check CloudWatch logs
- Both: Verify env variables are set

## Project Structure

### Root Projects
```
/projects/
├── call-records/          # Original project (file-based)
├── gemini-transcriber/    # Shared library (extracted)
└── telegram-diary-bot/    # This project (Telegram bot)
```

### Shared Library
`gemini-transcriber/` is a standalone package that:
- Handles Gemini API communication
- Validates audio formats
- Returns transcriptions
- Can be used in other projects

To use in another project:
```
pip install /path/to/gemini-transcriber
# or from GitHub
pip install git+https://github.com/yourname/gemini-transcriber.git
```

## Configuration

### Environment Variables
```bash
TELEGRAM_BOT_TOKEN=          # Required: From BotFather
GEMINI_API_KEY=              # Required: From Google AI Studio
```

### Advanced Settings
Edit `main.py` to customize:
- Polling interval (currently: continuous)
- Timeout duration (currently: 60 seconds)
- Error messages
- Response format

## Deployment Checklist

- [ ] Create Telegram bot with BotFather
- [ ] Get Gemini API key
- [ ] Choose hosting platform
- [ ] Copy `.env.example` → `.env`
- [ ] Add credentials to `.env`
- [ ] Run tests locally
- [ ] Follow deployment guide
- [ ] Test with real audio
- [ ] Monitor logs for errors

## Performance

**Typical Response Time:**
- Local: <10 seconds (depends on audio length)
- PythonAnywhere: 15-30 seconds (with polling)
- AWS Lambda: <5 seconds (with webhooks)

**Supported Audio Length:**
- Default: Up to 25 minutes
- Large files: May need Files API (future enhancement)

## Cost

### Free Tier
- **PythonAnywhere**: Truly free (100MB storage)
- **AWS Lambda**: 1M requests/month free
- **Gemini API**: $0.075 per 1M input tokens (very cheap)

### Estimated Monthly Cost
- Under 100 transcriptions/day: **$0**
- 1000 transcriptions/day: **$1-2/month**

## Future Enhancements

- [ ] Multi-language support
- [ ] Speaker diarization (identify different speakers)
- [ ] Save transcription history
- [ ] Support for files >25MB (using Files API)
- [ ] Audio quality improvement
- [ ] Batch processing
- [ ] Database integration

## Contributing

To improve this project:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Security

⚠️ **Important:**
- Never commit `.env` to git
- Store API keys securely
- Use environment variables in production
- Rotate tokens if exposed

## Support

For issues:
1. Check [Troubleshooting](#troubleshooting)
2. Review deployment guide
3. Check bot logs
4. Open an issue on GitHub

## License

MIT License - feel free to use and modify

## Resources

- [Telegram Bot API](https://core.telegram.org/bots)
- [python-telegram-bot docs](https://python-telegram-bot.readthedocs.io/)
- [Google Gemini API](https://ai.google.dev/)
- [PythonAnywhere](https://www.pythonanywhere.com/)
- [AWS Lambda](https://aws.amazon.com/lambda/)

---

**Built with:**
- python-telegram-bot 22.5+
- google-genai 1.50+
- Python 3.8+

Happy transcribing! 🎙️✨
