import os
import discord
from discord.ext import commands
import wavelink
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()  # Enable all intents
        
        super().__init__(
            command_prefix='!',  # Fallback prefix
            intents=intents,
            application_id=int(os.getenv('DISCORD_CLIENT_ID'))
        )

    async def setup_hook(self):
        # Initialize wavelink for version 3.x
        try:
            print(f"Using wavelink version: {wavelink.__version__}")
            
            # Wavelink 3.x connection method
            nodes = [
                wavelink.Node(
                    uri='http://localhost:4400',
                    password='youshallnotpass'
                )
            ]
            
            # Connect to nodes
            await wavelink.Pool.connect(nodes=nodes, client=self)
            print("Successfully connected to Lavalink server using wavelink 3.x")
        except Exception as e:
            print(f"Failed to connect to Lavalink server: {e}")
        
        # Load all cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"Loaded extension: {filename}")
                except Exception as e:
                    print(f"Failed to load extension {filename}: {e}")

    async def on_ready(self):
        print(f'Logged in as {self.user.name} ({self.user.id})')
        print('------')
        
        # Sync commands with Discord
        try:
            # Sync to all guilds - this is critical for slash commands to work
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s) globally")
            
            # Print all registered commands for debugging
            print("Registered commands:")
            for command in self.tree.get_commands():
                print(f"- /{command.name}")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

# Create bot instance
bot = MusicBot()

# Run the bot
bot.run(os.getenv('DISCORD_CLIENT_TOKEN'))