#import discord
from discord.ext import commands

#creates a variable for the bot and sets the prefix that will be used for commands
client = commands.Bot(command_prefix='~')

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_member_join(member):
    print(f"{member} has joined the server")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the building")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)} ms")

@client.command(aliases=["testing"])
async def _8Ball(ctx, *, question):
    responses = ["no"]
    await ctx.send(f"Question: {question}\nAnswer: {responses}")

@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)
    
client.run("NzIyNTQ5NjM1ODU5NzQyODUw.XuktTg.dL0Zu5GWys_9IV7jVAFNXoDoMCA")