"""
Train CampusBot with the assignment sample dialogue plus English corpus data.

Usage:
    python manage.py train
"""

from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from django.core.management.base import BaseCommand

from chat.bot import get_chatbot

# Assignment example conversation from the ChatterBot documentation.
ASSIGNMENT_DIALOGUE = [
    "Good morning! How are you doing?",
    "I am doing very well, thank you for asking.",
    "You're welcome.",
    "Do you like hats?",
]


class Command(BaseCommand):
    help = "Train the ChatterBot instance with sample and corpus conversations."

    def handle(self, *args, **options):
        chatbot = get_chatbot()

        # ListTrainer maps each statement to the next statement in the list.
        list_trainer = ListTrainer(chatbot)
        list_trainer.train(ASSIGNMENT_DIALOGUE)

        # Corpus trainer loads prepared English greetings and small-talk.
        corpus_trainer = ChatterBotCorpusTrainer(chatbot)
        corpus_trainer.train(
            "chatterbot.corpus.english.greetings",
            "chatterbot.corpus.english.conversations",
        )

        self.stdout.write(self.style.SUCCESS("Training completed successfully."))
