# Flask-MAIL-with-CELERY

This app sends emails using `Flask-Mail` asynchronously through `celery`. It also provide email validation support with signed tokens.

# HOW TO TEST IT OUT

In terminal outside the app environment. Do the following:

- `pip install redis`
- `redis-server`

In another terminal in your virtual environment:

- `cd /path/to/project`

- `pip install -r requirements.txt`

- `python main.py`

In another terminal in your virual environment:

- `cd /path/to/project`

- `celery -A app.view.celery worker --loglevel=info`

# Endpoints

| Endpoint | Description |
| ---- | --------------- |
| [POST|GET: /](#) |  Input email address |
| [GET: /confirm-email/<token>](#) | Confirm email address |

