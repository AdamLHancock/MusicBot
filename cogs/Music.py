import asyncio

import discord
from discord.ext import commands

import youtube_dl
import os


ytdl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_opts = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_opts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, song_name=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        if song_name is not None:
            song_name = song_name + os.path.splitext(filename)[1]
            os.rename(filename, song_name)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_opts), data=data)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """~join [channel] - Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send(f'Now playing: {query}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def download(self, ctx, arg, *, url):
        """Downloads a song for the playlist"""

        await YTDLSource.from_url(url, loop=self.client.loop, song_name=arg)
        await ctx.send(f'Downloaded {arg}')

    # playlists are stored in folders with the ctx.author's name and accessed the same way
    @commands.command()
    async def list_playlist(self, ctx):
        """Lists the songs on the playlist"""
        songs = ''
        i = 1
        for song in playlist:
            songs = f'{songs}{i}. {song} \n'
            i = i + 1
        await ctx.send(f'The Playlist:\n{songs}')

    @commands.command()
    async def saved_songs(self, ctx):
        list_of_songs = ''
        for files in os.listdir('./'):
            if os.path.splitext(files)[1] == '.webm':
                list_of_songs = list_of_songs + files + '\n'
        
        await ctx.send(f'The list of songs:\n{list_of_songs}')

    @commands.command()
    async def add_to_playlist(self, ctx, song):
        for songs in playlist:
            if songs == song:
                return await ctx.send(f'{song} is already in the playlist')
        
        playlist.append(song)
        await ctx.send(f'{song} has been added to the playlist')

    @commands.command()
    async def play_from_playlist(self, ctx, num: int):
        num = num - 1
        self.play(ctx, query=playlist[num])

    @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        """Pauses the song currently playing"""

        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('Music has been paused')
        else:
            return await ctx.send('Bot is paused')

    @commands.command()
    async def resume(self, ctx):
        """Resumes the song currently playing"""

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('Music has been resumed')
        else:
            return await ctx.send('Bot is not paused')

    @pause.before_invoke
    @resume.before_invoke
    async def confirm_in_voice(self, ctx):
        if ctx.voice_client is None or self.client.voice.channel is not ctx.author.voice.channel:
            await ctx.send(f'Bot is not in {ctx.author.voice.channel} with {ctx.author}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect() 
    

def setup(client):
    client.add_cog(Music(client))