# Cloud-Cord
===========

Cloud-Cord is a Python + Discord bot utility that uses Discord text channels as file storage.
It can split large files, upload them as attachments to a dedicated channel, and later download and reconstruct the original file.

This project is CLI-driven and runs inside a Discord bot process (it does NOT use slash commands).

DISCLAIMER
----------

This project uses Discord as a file storage backend.
Use only on private servers and at your own risk.

FEATURES
--------

- Upload files to discord 
- List uploaded files (technically?)
- Download uploaded files

REQUIREMENTS
------------

- Python 3.9 or newer
- A Discord bot token
- A Discord server where the bot has:
  - Read Message History
  - Send Messages
  - Attach Files
  - Manage Channels

Python dependencies:
- discord.py
- python-dotenv

SETUP
-----

1) Clone the repository

git clone https://github.com/kbzx3/cloud-cord.git
cd cloud-cord

2) Install dependencies

pip install -r requirements.txt

3) Create keys.env

Create a file named keys.env with the following content:

DISCORD_TOKEN=your_bot_token_here

NOTE: The filename must be exactly keys.env.

4) Set your guild ID

Edit main.py and replace:

guild_id = YOUR_GUILD_ID

5) Run the bot

python main.py

HOW IT WORKS
------------

UPLOAD:
- The file is split into 8 MB binary chunks
- A new text channel is created using the file name
- Each chunk is uploaded as an attachment
- Temporary chunk files are deleted after upload

DOWNLOAD:
- Attachments are downloaded and sorted by filename
- Files are concatenated byte-for-byte
- The original file is reconstructed

Reconstructed files are saved as:

<channel_name>ccd<original_extension>

Example:
movieccd.mp4

MENU OPTIONS
------------

0) Upload file
1) Download file
2) List channels
exit) Quit

LICENSE
-------

MIT License