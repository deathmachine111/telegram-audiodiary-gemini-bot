# Local Testing Guide

## Prerequisites ✅
- [x] Virtual environment created
- [x] Dependencies installed
- [x] `.env` file with credentials
- [ ] Bot running and connected

## Step 1: Verify Your .env File

Before starting, confirm your `.env` has both tokens:

```bash
cat .env
# Should show:
# TELEGRAM_BOT_TOKEN=<your_token>
# GEMINI_API_KEY=<your_key>
```

## Step 2: Start the Bot

```bash
# Windows
"C:\Users\soumy\projects\telegram-diary-bot\venv\Scripts\python.exe" main.py

# Or activate venv first:
venv\Scripts\activate
python main.py
```

**You should see:**
```
🤖 Bot started! Press Ctrl+C to stop.
```

## Step 3: Test in Telegram

Open Telegram and find your bot (search by the name you gave it to BotFather).

### Test 1: Send `/start` command
Bot should reply with welcome message:
```
🎙️ Welcome to Audio Diary Transcriber!

Send me an audio file and I'll transcribe it to English romanized text.
Supported formats: MP3, M4A, WAV, AIFF, OGG, FLAC
```

### Test 2: Send `/help` command
Bot should reply with help message.

### Test 3: Send an Audio File

**Option A: Use a real audio file**
1. Find an audio file on your computer (MP3, M4A, etc.)
2. Send it to your bot via Telegram
3. Wait for transcription
4. Bot should reply with transcribed text

**Option B: Record a voice message**
1. Long-press the microphone icon in Telegram
2. Record a message in Bengali/Hindi/English
3. Send it
4. Bot should transcribe it

### Expected Response
```
✅ Transcription:

[Your transcribed text in English romanized format]
```

## Troubleshooting

### Bot doesn't respond to `/start`

**Check 1: Is bot running?**
```
# Terminal should show: 🤖 Bot started!
```

**Check 2: Wrong token?**
- Copy token again from BotFather
- Update `.env`
- Restart bot

**Check 3: Network issue?**
- Check internet connection
- Ensure firewall allows Python

### Bot responds but transcription is empty

**Check 1: Valid audio format?**
- Supported: MP3, M4A, WAV, AIFF, OGG, FLAC
- Try a different file

**Check 2: Audio quality?**
- Audio should be clear (not too quiet/noisy)
- Try recording again

**Check 3: Gemini API issue?**
- Check API key is valid
- Check API has available quota
- Look for errors in terminal

### Bot crashes or freezes

**Common issues:**
1. Missing dependency
   ```bash
   pip install -r requirements.txt
   ```

2. Wrong Python version
   ```bash
   python --version  # Should be 3.8+
   ```

3. Timeout (audio too long)
   - Files >25MB may fail
   - Try shorter audio first

## Understanding the Logs

When bot is running, watch the terminal for:

**Good signs:**
```
⏳ Processing your audio...    [User sent audio]
Error transcribing audio: ...  [Shows what went wrong if issue]
✅ Transcription sent          [Success]
```

**Bad signs:**
```
Error: GEMINI_API_KEY not provided    → Check .env
Error: TELEGRAM_BOT_TOKEN not found   → Check .env
ConnectionError                       → Check internet
```

## Testing Different Scenarios

### Test 1: Bengali Audio
- Record: "আমার দিনটি খুব ভালো ছিল"
- Expected: Romanized English equivalent

### Test 2: Mixed Language
- Record: "Amar din khub valo chilo, it was a great day"
- Expected: Should handle both languages

### Test 3: Clear Speech
- Record clearly into microphone
- Expected: Accurate transcription

### Test 4: Quiet Audio
- Record quietly (test edge case)
- Expected: May have errors or blanks

## Performance Expectations

**Typical timings (local, with polling):**
- `/start` command: <1 second
- Audio upload: 2-5 seconds
- Gemini processing: 5-20 seconds (depends on audio length)
- **Total response: 10-30 seconds**

## Next Steps After Testing

When everything works locally:

1. ✅ Verify `/start` works
2. ✅ Verify `/help` works
3. ✅ Verify audio transcription works
4. ✅ Check response quality
5. → Ready to deploy!

Choose deployment platform:
- **PythonAnywhere**: See `DEPLOY_PYTHONANYWHERE.md`
- **AWS Lambda**: See `DEPLOY_AWS_LAMBDA.md`

## Tips for Best Results

1. **Clear Audio**: Speak clearly near the microphone
2. **Good Microphone**: Built-in mics work, headset is better
3. **Short Clips**: Test with <30 seconds first
4. **One Speaker**: Single speaker works best
5. **No Background Noise**: Quiet environment works best

## Monitoring While Testing

Keep terminal open to see logs:
```
[INFO] User ID: 12345 sent audio
[INFO] Downloading audio file...
[INFO] Transcribing with Gemini...
[INFO] Sending transcription...
```

## Session Example

```bash
C:\Users\soumy\projects\telegram-diary-bot> python main.py
🤖 Bot started! Press Ctrl+C to stop.

# [User sends /start command in Telegram]
# [Bot responds with welcome message]

# [User sends audio file]
[INFO] Processing audio from user 12345
[INFO] Transcription complete
[INFO] Sent to user

# [Wait 30 seconds...]
# [You see transcription in Telegram]

# Ctrl+C to stop bot
^C
Bot stopped.
```

## Common Questions

**Q: How long does transcription take?**
A: 10-30 seconds depending on audio length

**Q: Will it work offline?**
A: No, it needs internet for Gemini API

**Q: Can I test without Telegram?**
A: Not easily - bot is Telegram-specific. But you can test the transcriber directly:
```python
from gemini_transcriber import GeminiTranscriber
transcriber = GeminiTranscriber(api_key="YOUR_KEY")
text = transcriber.transcribe("audio.mp3", prompt="Transcribe this")
print(text)
```

**Q: Do I need to keep terminal open?**
A: Yes, while testing. When deployed, it runs in the cloud.

**Q: Can multiple people use it?**
A: Yes, bot handles multiple users simultaneously.

---

**Ready to test? 🚀**

1. Make sure `.env` is filled
2. Run `python main.py`
3. Open Telegram
4. Send `/start` to your bot
5. Send an audio file
6. See the magic happen! ✨
