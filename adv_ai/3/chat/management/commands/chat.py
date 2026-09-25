"""
Start an interactive terminal chat session with CampusBot.

Usage:
    python manage.py chat
"""

from django.core.management.base import BaseCommand

from chat.bot import get_chatbot
from chat.conversation import run_terminal_chat


class Command(BaseCommand):
    help = "Open a terminal client to chat with the trained ChatterBot."

    def handle(self, *args, **options):
        # read_only keeps trained replies stable during a demo session.
        chatbot = get_chatbot(read_only=True)
        run_terminal_chat(chatbot)
