# K25MusicBot
Discord bot project under development. Kaam kinda bhari rn tho fr icl

# Discord Music Bot

A feature-rich Discord music bot built with discord.py and wavelink that allows users to play music in voice channels.

## Features

- Play music from various sources
- Queue management
- Volume control
- Skip, pause, and resume functionality
- Slash commands support

## Prerequisites

- Python 3.8 or higher
- Java 11 or higher (for Lavalink server)
- A Discord bot token
- A Discord application with bot permissions

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following content:
```
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_CLIENT_TOKEN=your_discord_bot_token
```

4. Download and set up Lavalink:
   - The repository includes `Lavalink.jar` (https://github.com/lavalink-devs/Lavalink/releases/tag/4.0.8) and `application.yml`
   - Make sure Java 11 or higher is installed
   - The Lavalink server will run on port 4400

## Running the Bot

1. Start the Lavalink server:
```bash
java -jar Lavalink.jar
```

2. In a separate terminal, start the Discord bot:
```bash
python bot.py
```

## Available Commands

The bot uses slash commands. Here are the main commands:

- `/play <query>` - Play a song or add it to the queue
- `/skip` - Skip the current song
- `/stop` - Stop playing and clear the queue
- `/pause` - Pause the current song
- `/resume` - Resume the paused song
- `/queue` - Show the current queue
- `/volume <0-100>` - Adjust the volume

## Project Structure

```
├── bot.py              # Main bot file
├── cogs/              # Command modules
│   └── music.py       # Music-related commands
├── Lavalink.jar       # Lavalink server
├── application.yml    # Lavalink configuration
├── requirements.txt   # Python dependencies
└── .env              # Environment variables (create this)
```

## Dependencies

- discord.py >= 2.3.2
- python-dotenv >= 1.0.0
- wavelink >= 3.2.0

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
