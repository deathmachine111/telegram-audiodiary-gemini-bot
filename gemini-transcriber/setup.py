from setuptools import setup, find_packages

setup(
    name="gemini-transcriber",
    version="0.1.0",
    description="Reusable Gemini audio transcription library",
    packages=find_packages(),
    install_requires=[
        "google-genai>=1.40.0",
    ],
    python_requires=">=3.8",
)
