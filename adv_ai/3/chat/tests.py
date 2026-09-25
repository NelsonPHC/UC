"""
Tests for the terminal conversation loop.

A dummy bot is used so tests do not require spaCy models or a trained database.
"""

from django.test import SimpleTestCase

from chat.conversation import run_terminal_chat


class DummyBot:
    """Minimal stand-in for chatterbot.ChatBot used in unit tests."""

    name = "TestBot"

    def get_response(self, user_input):
        return f"echo:{user_input}"


class ConversationLoopTests(SimpleTestCase):
    def test_quit_ends_the_session(self):
        replies = []
        inputs = iter(["Hello", "quit"])

        run_terminal_chat(
            DummyBot(),
            stdin_input=lambda _prompt: next(inputs),
            stdout_write=replies.append,
        )

        self.assertIn("bot: echo:Hello", replies)
        self.assertIn("Goodbye.", replies)

    def test_blank_lines_are_ignored(self):
        replies = []
        inputs = iter(["", "Hi", "exit"])

        run_terminal_chat(
            DummyBot(),
            stdin_input=lambda _prompt: next(inputs),
            stdout_write=replies.append,
        )

        self.assertEqual(sum(1 for line in replies if line.startswith("bot:")), 1)
        self.assertIn("bot: echo:Hi", replies)
