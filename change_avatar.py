import os

from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

pfp_path = "avatar.png"

fp = open(pfp_path, 'rb')
pfp = fp.read()

@client.event
async def on_ready():
    # await client.user.edit(avatar=pfp)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="d-_-b"))

client.run(TOKEN)