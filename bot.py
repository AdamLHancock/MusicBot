#import discord
from discord.ext import commands

#creates a variable for the bot and sets the prefix that will be used for commands
client = commands.Bot(command_prefix='~')

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')

@client.event
async def on_member_remove(member):
    print(f"{member} has left the building")

client.run("NzIyNTQ5NjM1ODU5NzQyODUw.XuktTg.dL0Zu5GWys_9IV7jVAFNXoDoMCA")