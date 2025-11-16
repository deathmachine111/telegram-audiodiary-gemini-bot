# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy entire project context (including gemini-transcriber)
COPY . .

# Install local gemini-transcriber package first
RUN pip install --no-cache-dir -e ./gemini-transcriber

# Install other dependencies (without gemini-transcriber line)
RUN pip install --no-cache-dir python-telegram-bot[all]>=21.0 python-dotenv>=1.0.0

# Run the bot
CMD ["python", "main.py"]
