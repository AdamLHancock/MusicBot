import discord
from discord.ext import commands

class CommandCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('The bot is online')

    #Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong')

def setup(client):
    client.add_cog(CommandCog(client))