"""
Shared ChatterBot factory for this Django project.

Creating ChatBot instances in one place keeps the storage adapter, logic
adapters, and bot name consistent between training and the terminal client.
"""

from chatterbot import ChatBot
from django.conf import settings


def get_chatbot(**overrides):
    """
    Build a ChatBot using CHATTERBOT settings.

    Extra keyword arguments override settings (for example, read_only=True
    during chat so a live session does not overwrite trained responses).
    """
    config = dict(settings.CHATTERBOT)
    config.update(overrides)
    return ChatBot(**config)
