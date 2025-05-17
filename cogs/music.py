import discord
from discord import app_commands
from discord.ext import commands
import wavelink
from typing import Optional

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # This listener is important for debugging
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Music cog is ready!")

    @app_commands.command(name="play", description="Play a song")
    async def play(self, interaction: discord.Interaction, query: str):
        if not interaction.user.voice:
            return await interaction.response.send_message("You must be in a voice channel!", ephemeral=True)

        # Get the voice channel
        voice_channel = interaction.user.voice.channel
        
        try:
            # Wavelink 3.x search method
            # First, defer the response since search might take time
            await interaction.response.defer(ephemeral=False)
            
            # Get or create player - wavelink 3.x method
            if not interaction.guild.voice_client:
                # Connect to voice channel
                player = await voice_channel.connect(cls=wavelink.Player)
            else:
                player = interaction.guild.voice_client

            # Search for the track using wavelink 3.x method
            search_query = wavelink.Playable.search(query)
            tracks = await search_query
            
            if not tracks:
                return await interaction.followup.send("No tracks found!")
            
            track = tracks[0]  # Get the first track from search results
            
            # Play the track or add to queue
            if player.playing:
                # Add to queue
                await player.queue.put_wait(track)
                await interaction.followup.send(f"Added to queue: **{track.title}**")
            else:
                # Play immediately
                await player.play(track)
                await interaction.followup.send(f"Now playing: **{track.title}**")
                
        except Exception as e:
            # If response wasn't deferred yet, defer it
            try:
                await interaction.response.defer(ephemeral=True)
            except:
                pass
                
            await interaction.followup.send(f"Error: {str(e)}")
            print(f"Play command error: {e}")

    @app_commands.command(name="stop", description="Stop the current playback")
    async def stop(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not playing anything!", ephemeral=True)
        
        player = interaction.guild.voice_client
        await player.disconnect()
        await interaction.response.send_message("Stopped playback and disconnected.")

    @app_commands.command(name="pause", description="Pause the current playback")
    async def pause(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not playing anything!", ephemeral=True)
        
        player = interaction.guild.voice_client
        if player.paused:
            return await interaction.response.send_message("Already paused!", ephemeral=True)
        
        await player.pause()
        await interaction.response.send_message("Paused playback.")

    @app_commands.command(name="resume", description="Resume the current playback")
    async def resume(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not playing anything!", ephemeral=True)
        
        player = interaction.guild.voice_client
        if not player.paused:
            return await interaction.response.send_message("Not paused!", ephemeral=True)
        
        await player.resume()
        await interaction.response.send_message("Resumed playback.")

    @app_commands.command(name="skip", description="Skip the current song")
    async def skip(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not playing anything!", ephemeral=True)
        
        player = interaction.guild.voice_client
        await player.stop()
        await interaction.response.send_message("Skipped current song.")

    @app_commands.command(name="queue", description="Show the current queue")
    async def queue(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not playing anything!", ephemeral=True)
        
        player = interaction.guild.voice_client
        
        # Check if queue is empty - wavelink 3.x uses player.queue
        if player.queue.empty():
            return await interaction.response.send_message("Queue is empty!", ephemeral=True)
        
        # Get tracks from queue using wavelink 3.x method
        upcoming_tracks = player.queue.all()
        queue_list = "\n".join([f"{i+1}. {track.title}" for i, track in enumerate(upcoming_tracks)])
        
        await interaction.response.send_message(f"**Current Queue:**\n{queue_list}")

    @app_commands.command(name="volume", description="Set the volume (0-100)")
    async def volume(self, interaction: discord.Interaction, volume: int):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not playing anything!", ephemeral=True)
        
        if not 0 <= volume <= 100:
            return await interaction.response.send_message("Volume must be between 0 and 100!", ephemeral=True)
        
        player = interaction.guild.voice_client
        # Wavelink 3.x uses volume as a property
        await player.set_volume(volume)
        await interaction.response.send_message(f"Volume set to {volume}%")

    @app_commands.command(name="nowplaying", description="Show the currently playing song")
    async def nowplaying(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not playing anything!", ephemeral=True)
        
        player = interaction.guild.voice_client
        if not player.playing:
            return await interaction.response.send_message("Nothing is currently playing!", ephemeral=True)
        
        # In wavelink 3.x, current track is player.current
        track = player.current
        await interaction.response.send_message(f"**Now Playing:** {track.title}")

async def setup(bot):
    await bot.add_cog(Music(bot))
