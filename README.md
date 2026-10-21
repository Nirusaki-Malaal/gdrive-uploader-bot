<p align="center">
  <img src="assets/logo.svg" alt="gdrive-uploader-bot logo" width="540">
</p>

# gdrive-uploader-bot

Asynchronous Telegram bot streaming chat media directly to Google Drive and Shared Team Drives with per-user OAuth2 sessions.

## Architecture

* **Worker Queue**: Pyrogram-based concurrency worker serializing concurrent file downloads.
* **OAuth Session Store**: MongoDB database storing user credentials and custom Team Drive destination IDs.
* **Stream Bridge**: Direct chunked uploader to Google Drive API v3 without saturating local disk space.
* **Web Generator**: Built-in template generator creating HTML episode indexes for uploaded folder hierarchies.

## Module Layout

* `bot/__main__.py`: Application bootstrap and top-level command handlers.
* `bot/__init__.py`: Pyrogram client initialization, configuration loading, and MongoDB connection.
* `bot/plugins/upload.py`: Google Drive API streaming upload worker.
* `bot/plugins/authorise.py`: OAuth2 consent flows and Team Drive assignment.
* `bot/plugins/utils.py`: Asynchronous queue manager and progress calculation.
* `bot/plugins/html.py`: Drive directory listing and HTML page synthesis.

## Configuration

Set the following variables in `config.env` or environment variables:

| Variable | Description |
| :--- | :--- |
| `API_ID` | Telegram API ID from my.telegram.org |
| `API_HASH` | Telegram API Hash from my.telegram.org |
| `BOT_TOKEN` | Bot token from @BotFather |
| `DATABASE_URL` | MongoDB connection URI |
| `OWNER_ID` | Telegram user ID of authorized administrator |

## Installation and Execution

```bash
pip install -r requirements.txt
chmod +x start.sh
./start.sh
```

## License

GPL-3.0-or-later. See LICENSE for details.
