#!/usr/bin/env python
"""
Standalone terminal client for the Django + ChatterBot chatbot.

This script loads Django settings so ChatterBot can use DjangoStorageAdapter
and the same SQLite database as the rest of the project.

Usage (from the project root, with the virtual environment activated):
    python terminal_client.py
"""

import os

import django

# Point Django at this project's settings before importing models or ChatBot.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_project.settings")
django.setup()

from chat.bot import get_chatbot  # noqa: E402
from chat.conversation import run_terminal_chat  # noqa: E402


def main():
    """Create the bot and start the interactive prompt loop."""
    chatbot = get_chatbot(read_only=True)
    run_terminal_chat(chatbot)


if __name__ == "__main__":
    main()
