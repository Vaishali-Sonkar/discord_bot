# discord_bot

A small Discord bot project with  AI integration.

Features
- Connects to Discord and runs a bot defined in `bot.py`.
- Lightweight AI helper logic in `agent.py` for processing or generating responses.

Requirements
- Python 3.10+ (Windows tested).
- A Discord bot token (create one at the Discord Developer Portal).
- Optional: any third-party packages listed in `requirements.txt` if present.

Setup
1. Create and activate a virtual environment:

	- PowerShell (Windows):

	  ```powershell
	  python -m venv venv
	  .\venv\Scripts\Activate.ps1
	  ```

2. Install dependencies (if you have a `requirements.txt`):

	```powershell
	pip install -r requirements.txt
	```

3. Provide configuration:

	- Create a `.env` file or set environment variables with your Discord token, e.g. `DISCORD_TOKEN=your_token_here`.

Running
- Start the bot:

  ```powershell
  python bot.py
  ```

File overview
- `bot.py`: Main entrypoint that connects to Discord and registers commands/events.
- `agent.py`: AI helper utilities used by the bot to generate or process responses.

Notes
- This README is intentionally brief. If you want, I can add command documentation, example `.env` templates, or a `requirements.txt` based on the code.

License
- Add a license file if you plan to make this project public.
