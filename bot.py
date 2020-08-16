import discord
from discord.ext import commands
import os
from token.py import bot_token

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

client = commands.Bot(command_prefix = '-')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(ctx)

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print(ctx)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(bot_token)
