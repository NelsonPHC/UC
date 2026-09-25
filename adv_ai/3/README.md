# Terminal Chat Client (Django + ChatterBot)

A terminal client that chats with a machine-learning conversational bot
powered by [ChatterBot](https://pypi.org/project/ChatterBot/) and stored
through Django's ORM.

Typical session after training:

```
user: Good morning! How are you doing?
bot: I am doing very well, thank you for asking.
user: You're welcome.
bot: Do you like hats?
```

## Setup

Python 3.10+ is required (ChatterBot 1.2.x).

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python manage.py migrate
python manage.py train
```

## Chat

Either of these starts the same terminal client:

```bash
python manage.py chat
python terminal_client.py
```

Type `quit` or `exit`, or press Ctrl-C, to leave the session.

## Tests

```bash
python manage.py test chat
```

## Project layout

See `MANIFEST.txt` for the full file list. ChatterBot statements are stored in
SQLite (`db.sqlite3`) by `chatterbot.storage.DjangoStorageAdapter`.
