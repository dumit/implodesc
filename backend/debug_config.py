#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from implodesc.core.config import Settings

try:
    print("Testing configuration...")
    settings = Settings()
    print("✅ Configuration loaded successfully!")
    print(f"OpenAI key present: {bool(settings.openai_api_key)}")
    print(f"CORS origins: {settings.cors_origins}")
    print(f"Allowed hosts: {settings.allowed_hosts}")
except Exception as e:
    print(f"❌ Configuration failed: {e}")
    print(f"Current .env CORS_ORIGINS: {os.getenv('CORS_ORIGINS')}")
    print(f"Current .env ALLOWED_HOSTS: {os.getenv('ALLOWED_HOSTS')}")