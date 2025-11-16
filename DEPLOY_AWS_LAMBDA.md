# Deploy to AWS Lambda (Serverless & Free Tier Eligible)

## Why AWS Lambda?
- ✅ Very cheap (free tier: 1M requests/month)
- ✅ No server management
- ✅ Fast response times with webhooks
- ✅ Auto-scales for high traffic
- ✅ Pay only for what you use

## Architecture
```
Telegram → API Gateway → Lambda Function → Gemini API
```

## Setup Steps

### 1. Install AWS CLI and Docker
```bash
# Windows - Download and install:
# https://aws.amazon.com/cli/
# https://www.docker.com/products/docker-desktop/

# Verify installation
aws --version
docker --version
```

### 2. Create AWS Account
- Go to https://aws.amazon.com
- Sign up (free tier available)
- Create IAM user with Lambda + API Gateway permissions

### 3. Create Lambda Function Directory
```bash
mkdir telegram-diary-lambda
cd telegram-diary-lambda
```

### 4. Create Lambda Handler
Create `lambda_handler.py`:
```python
"""AWS Lambda handler for Telegram bot."""
import json
import os
import tempfile
import logging
from pathlib import Path
from urllib.parse import urljoin

# Add layers to path (if using dependencies layer)
import sys
sys.path.insert(0, '/opt/python')

from telegram import Update, User, Chat, Message
from telegram.ext import Application
from gemini_transcriber import GeminiTranscriber

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Bot handlers (same as main.py handlers)
async def handle_audio(update: Update, context):
    """Handle audio transcription."""
    try:
        processing_msg = await update.message.reply_text("⏳ Processing your audio...")

        file = await update.message.audio.get_file()
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_path = tmp_file.name
            await file.download_to_drive(custom_path=tmp_path)

        try:
            transcriber = GeminiTranscriber(api_key=os.getenv("GEMINI_API_KEY"))
            prompt = (
                "This is an audio diary recording in Bengali. "
                "Hindi or English words may be used. "
                "Transcribe this into English romanized fonts. "
                "Only output the transcription and nothing else."
            )

            transcript = transcriber.transcribe(tmp_path, prompt=prompt)

            if transcript:
                await processing_msg.edit_text(f"✅ Transcription:\n\n{transcript}")
            else:
                await processing_msg.edit_text("❌ Failed to transcribe.")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def lambda_handler(event, context):
    """Handle Lambda invocation from API Gateway webhook."""
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        # Parse Telegram webhook update
        update_data = json.loads(event.get('body', '{}'))
        update = Update.de_json(update_data, Application.DEFAULT_BOT)

        # Create app with your token
        app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

        # Process update
        await app.process_update(update)

        return {
            'statusCode': 200,
            'body': json.dumps('OK')
        }
    except Exception as e:
        logger.error(f"Lambda error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
```

### 5. Create requirements.txt
```
python-telegram-bot[all]>=21.0
gemini-transcriber @ git+https://github.com/yourusername/gemini-transcriber.git
```

### 6. Build Lambda Package
```bash
# Create package directory
mkdir package

# Install dependencies
pip install -r requirements.txt -t package/

# Copy your code
cp lambda_handler.py package/
cp -r ../gemini-transcriber package/

# Create zip
cd package
zip -r9 ../lambda_function.zip .
cd ..
```

### 7. Deploy with AWS CLI
```bash
# Create IAM role (do once)
aws iam create-role \
  --role-name telegram-bot-role \
  --assume-role-policy-document file://trust-policy.json

# Attach basic Lambda execution policy
aws iam attach-role-policy \
  --role-name telegram-bot-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Create function
aws lambda create-function \
  --function-name telegram-diary-bot \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT_ID:role/telegram-bot-role \
  --handler lambda_handler.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --timeout 60 \
  --environment Variables="TELEGRAM_BOT_TOKEN=YOUR_TOKEN,GEMINI_API_KEY=YOUR_KEY"
```

### 8. Create API Gateway Webhook
```bash
# Create API Gateway
aws apigateway create-rest-api --name "telegram-bot-api"

# Create POST method pointing to Lambda
# (Easier via AWS Console: API Gateway > Create > Lambda)
```

### 9. Set Telegram Webhook
```bash
curl -X POST https://api.telegram.org/botYOUR_TOKEN/setWebhook \
  -H "Content-Type: application/json" \
  -d '{"url": "https://YOUR_API_GATEWAY_URL/webhook"}'
```

### 10. Test
Send audio to your bot on Telegram!

## Cost Estimation
- Free tier: 1M requests/month (handles ~33K daily messages)
- Typical cost: $0.20/month (if over free tier)

## Monitoring
```bash
# View logs
aws logs tail /aws/lambda/telegram-diary-bot --follow

# Monitor invocations
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=telegram-diary-bot \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600
```

## Limitations
- 900 second timeout max (15 mins)
- Audio processing must finish within timeout
- Cold start adds ~1-2 second delay

## Better Alternative: Use python-telegram-bot async directly

For production, consider using the bot's application-level async support with AWS Lambda directly instead of the handler pattern above.
