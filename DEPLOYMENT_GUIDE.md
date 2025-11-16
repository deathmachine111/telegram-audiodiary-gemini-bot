# Deployment Guide - Choose Your Option

## Quick Comparison

| Platform | Ease | Cost | Speed | Best For |
|----------|------|------|-------|----------|
| **PythonAnywhere** | ⭐⭐⭐⭐⭐ | Free | Slow (polling) | Testing, hobby projects |
| **AWS Lambda** | ⭐⭐⭐ | Very cheap | Fast (webhooks) | Production, scaling |
| **Railway** | ⭐⭐⭐⭐ | $5/mo credit | Fast | Growing projects |
| **Heroku** | ⭐⭐⭐⭐ | $5+/mo | Fast | Easy deployment |

## Recommendation by Use Case

### I just want to test it
→ **PythonAnywhere** - Fastest setup, free tier, no credit card needed

### I expect heavy usage
→ **AWS Lambda** - Cheapest at scale, handles 1000+ messages/day free

### I want easy deployment + some free tier
→ **Railway** - Git-connected, modern, $5/month free credit

## Detailed Guides

- **[PythonAnywhere Setup](DEPLOY_PYTHONANYWHERE.md)** ← Start here if unsure
- **[AWS Lambda Setup](DEPLOY_AWS_LAMBDA.md)** ← For production

## Quick Start (PythonAnywhere)

1. Go to https://www.pythonanywhere.com → Sign up
2. In terminal:
   ```bash
   git clone <your-repo-url>
   cd telegram-diary-bot
   mkvirtualenv --python=/usr/bin/python3.11 bot
   pip install -r requirements.txt
   cp .env.example .env
   nano .env  # Add credentials
   ```
3. Create scheduled task to run `main.py` every hour
4. Done! Send audio to your bot

## Credentials You'll Need

Before deploying, have these ready:

1. **TELEGRAM_BOT_TOKEN**: Get from [@BotFather](https://t.me/botfather)
   - Chat with BotFather → /newbot → follow prompts
   - Copy the token

2. **GEMINI_API_KEY**: From your Google Cloud
   - Get from https://ai.google.dev/

## Testing Before Deployment

```bash
# Test locally
cd telegram-diary-bot
python main.py

# In another terminal, send test audio via curl:
curl -X POST https://api.telegram.org/botYOUR_TOKEN/sendAudio \
  -F "chat_id=YOUR_CHAT_ID" \
  -F "audio=@test_audio.mp3"
```

## Monitoring

After deployment, check:

**PythonAnywhere**:
- Web → Error logs
- Bash → Consoles (check scheduled task output)

**AWS Lambda**:
```bash
aws logs tail /aws/lambda/telegram-diary-bot --follow
```

## FAQ

**Q: Will it work 24/7?**
- PythonAnywhere: Yes (with polling)
- AWS Lambda: Yes (instant response with webhooks)

**Q: What's the latency?**
- PythonAnywhere: 5+ seconds per polling cycle
- AWS Lambda: <1 second with webhooks

**Q: Can I deploy for free?**
- Yes, both have free tiers
- PythonAnywhere: Truly free
- AWS Lambda: Free tier + free credit

**Q: How do I update the code after deployment?**
- PythonAnywhere: `git pull` in terminal or re-upload
- AWS Lambda: Redeploy zip file

## Next Steps

1. ✅ Choose a platform (PythonAnywhere recommended)
2. ✅ Get Telegram bot token
3. ✅ Get Gemini API key
4. ✅ Follow the detailed guide
5. ✅ Test by sending audio
6. ✅ Monitor logs

You got this! 🚀
