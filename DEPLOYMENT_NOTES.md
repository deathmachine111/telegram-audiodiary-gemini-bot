# Deployment Troubleshooting Notes

## Critical Errors & Solutions

### 1. **Invalid API Key Format**
**Error**: `400 INVALID_ARGUMENT: API key not valid`
**Cause**: User provided wrong API key format (looked like Telegram ID, not Gemini key)
**Solution**: Verify API key starts with `AIza` and is from Google AI Studio (makersuite.google.com/app/apikey)
**Prevention**: Always validate key format before deployment

### 2. **Missing Environment Variables in Docker**
**Error**: `Error: TELEGRAM_BOT_TOKEN not found in .env`
**Cause**: Fly.io secrets weren't propagated to running container. Using `load_dotenv()` fails silently in Docker without .env file
**Solution**:
- Always set secrets BEFORE deployment: `flyctl secrets set KEY=VALUE`
- Redeploy after secret changes: `flyctl deploy`
- Secrets are injected as env vars, not .env files
**Prevention**: Set secrets → Deploy in correct order

### 3. **Multiple Bot Instances (Telegram Conflict)**
**Error**: `409 Conflict: terminated by other getUpdates request`
**Cause**: Fly.io created standby machine (app + standby). Both polling Telegram with same token
**Solution**:
- Remove standby: `flyctl machines destroy <machine_id>`
- Update fly.toml with explicit process config
- Use single machine for polling bots
**Prevention**: For polling bots, configure only 1 machine in fly.toml

### 4. **Wrong Gemini API Endpoint (Experimental vs Production)**
**Error**: `404 NOT_FOUND: models/gemini-2.5-pro-exp-03-25 is not found`
**Cause**: Experimental endpoint name doesn't work with google-genai library v1beta API
**Solution**: Use `gemini-2.5-pro` (production endpoint - works with free tier API keys)
**Prevention**: Test model name locally before deployment

### 5. **Local Package Dependencies in Docker**
**Error**: pip couldn't resolve `gemini-transcriber @ file://...` paths during Docker build
**Cause**: Local file paths don't exist in Docker build context
**Solution**: Inline local package code directly into project instead of referencing it
**Prevention**: For Docker, copy code directly rather than using file:// references

## Key Deployment Checklist

- [ ] Test code locally with `python main.py` before deploying
- [ ] Verify all imports work: `python -m py_compile main.py`
- [ ] Check .env file is in .gitignore (secrets shouldn't be in repo)
- [ ] Set all required secrets BEFORE deployment
- [ ] Use correct model name (test locally first)
- [ ] For polling bots: ensure only 1 machine instance
- [ ] Verify Fly.io logs show "200 OK" responses, not errors

## Final Working Configuration

```
Model: gemini-2.5-pro (production endpoint)
API Key: AIza... format from Google AI Studio
Secrets: Set via flyctl secrets set before deployment
Machines: 1 active instance (remove standby)
Polling: getUpdates returns HTTP 200
```

## Time Wasters to Avoid

1. Don't try experimental endpoints without testing locally first
2. Don't assume secrets auto-update running containers (need redeploy)
3. Don't create multiple machines for polling bots
4. Don't use file:// paths in Docker - inline code instead
5. Don't skip local testing before each deployment
