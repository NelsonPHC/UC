"""
Reusable terminal conversation loop used by the management command and
the standalone terminal_client.py script.
"""

# Phrases that end a chat session (case-insensitive).
EXIT_COMMANDS = {"quit", "exit", "q"}


def run_terminal_chat(chatbot, stdin_input=input, stdout_write=print):
    """
    Read lines from the user and print bot replies until quit or Ctrl-C.

    stdin_input and stdout_write are injectable so the loop can be tested
    without a real terminal.
    """
    stdout_write(f"{chatbot.name} is ready. Type a message, or 'quit' to exit.")
    stdout_write("-" * 60)

    while True:
        try:
            user_input = stdin_input("user: ").strip()
        except (KeyboardInterrupt, EOFError):
            stdout_write("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in EXIT_COMMANDS:
            stdout_write("Goodbye.")
            break

        response = chatbot.get_response(user_input)
        stdout_write(f"bot: {response}")
