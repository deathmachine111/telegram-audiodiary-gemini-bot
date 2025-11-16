# Deploy to PythonAnywhere (Free & Easy)

## Why PythonAnywhere?
- ✅ Free tier available
- ✅ No infrastructure management
- ✅ Always-on 24/7 (with polling)
- ✅ Great for learning and hobby projects
- ✅ Simple setup

## Setup Steps

### 1. Create PythonAnywhere Account
- Go to https://www.pythonanywhere.com
- Sign up for free account
- Verify email

### 2. Clone Your Code
In PythonAnywhere terminal:
```bash
cd /home/your_username
git clone https://github.com/yourusername/telegram-diary-bot.git
cd telegram-diary-bot
```

(Or upload the project folder manually)

### 3. Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.11 telegram-bot
pip install -r requirements.txt
```

### 4. Add Credentials
```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

Add:
```
TELEGRAM_BOT_TOKEN=your_bot_token
GEMINI_API_KEY=your_gemini_key
```

Save with Ctrl+X, Y, Enter

### 5. Create Scheduled Task

In PythonAnywhere dashboard:
1. Go to **Web** section
2. Scroll to **Scheduled tasks**
3. Add new scheduled task:
   - Time: every hour (or more frequently)
   - Command:
     ```
     /home/your_username/telegram-diary-bot/venv/bin/python /home/your_username/telegram-diary-bot/run_bot.py
     ```

### 6. Create Bot Runner Script

Create `run_bot.py` in project root:
```python
"""Run bot once and exit (for scheduled tasks)."""
import subprocess
import sys

# Run bot for 55 minutes then exit
subprocess.run([sys.executable, "main.py"], timeout=3300)
```

### 7. Test
In terminal:
```bash
cd /home/your_username/telegram-diary-bot
/home/your_username/telegram-diary-bot/venv/bin/python main.py &
```

Send audio to your bot on Telegram - it should respond!

### Notes
- Free tier has limitations (100MB storage, limited CPU)
- Polling means slight delay in response
- For production, consider paid tier or upgrade to AWS Lambda

## Troubleshooting
- Check **Web > Error logs** for issues
- Use **Bash > Consoles > Always-on** for long-running tasks
