import discord
from discord.ext import commands
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

client = commands.Bot(command_prefix = '~')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('NzM5OTQ4NDQwMDQ5NDE4NDAw.Xyh4rw.pTZhvfwa9vJWfKK4qoWkIcVOlL8')
