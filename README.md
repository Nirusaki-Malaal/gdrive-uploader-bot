# GDrive Uploader Bot

A Telegram bot that uploads media from Telegram chats to Google Drive (including Team Drives / Shared Drives), with optional HTML episode-page generation.

## Features

- Queue-based uploads from Telegram documents/videos.
- Per-user Google OAuth storage in MongoDB.
- Team Drive configuration per user.
- Upload progress messages.
- Optional `/html2` flow to build a season/episode HTML page from a Drive folder.

## Project Structure

- `bot/__main__.py` — command handlers and upload queue entrypoint.
- `bot/__init__.py` — app configuration, logging, MongoDB setup, and Pyrogram client.
- `bot/plugins/upload.py` — Google Drive upload logic.
- `bot/plugins/authorise.py` — OAuth and Team Drive setup flows.
- `bot/plugins/utils.py` — queue worker and progress helpers.
- `bot/plugins/html.py` — HTML generation workflow.
- `start.sh` — run command (`python3 -m bot`).

## Requirements

- Python 3.10+ (recommended)
- Telegram Bot Token + API credentials from https://my.telegram.org
- MongoDB instance (Atlas/local)
- Google OAuth client JSON (`client_secrets.json`)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Edit `bot/__init__.py`:

- `Config.BOT_TOKEN`
- `Config.API_ID`
- `Config.API_HASH`
- `Config.AUTH_USERS` (list of allowed Telegram user IDs)
- `Config.DATABASE_URL`
- `Config.USERNAME` (Mongo DB name)

> Keep secrets out of source control in production. Use environment variables or secret managers.

## Running Locally

```bash
python3 -m bot
```

## Docker

Build:

```bash
docker build -t gdrive-uploader-bot .
```

Run:

```bash
docker run --rm -it gdrive-uploader-bot
```

## Bot Commands

- `/start` — health check message.
- `/uptime` — show bot uptime.
- `/authorise` — start Google OAuth flow.
- `/revoke` — remove saved Google OAuth credentials.
- `/td` — register Team Drive ID and Folder ID.
- `/tdvoke` — remove Team Drive configuration.
- `/upload` — upload the replied media message manually.
- `/clear` — clear current upload queue.
- `/logs` — fetch bot log file.
- `/html2` — generate season HTML page using Drive folder contents.

## Typical Setup Flow

1. Start bot and ensure your Telegram ID is in `AUTH_USERS`.
2. Run `/authorise` and complete OAuth.
3. Run `/td` and provide:
   - Team Drive ID
   - Team Drive Folder ID
4. Send video/document files to the bot chat.
5. Bot queues and uploads each file, then returns a Drive link.

## Troubleshooting

- **"Not Authorised"**
  - Re-run `/authorise`
  - Re-check Team Drive setup using `/td`
- **No uploads happen**
  - Confirm your user ID is in `AUTH_USERS`
  - Check `/logs`
- **Mongo errors**
  - Verify `DATABASE_URL` and DB permissions
- **Google auth failures**
  - Ensure `client_secrets.json` exists and OAuth consent settings are valid

## Notes

- This project stores OAuth credentials in MongoDB and writes a local temporary credential file per user ID.
- Generated HTML files are created temporarily and removed after sending.

## License

MIT (see `LICENSE`).
