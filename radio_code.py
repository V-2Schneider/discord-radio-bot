# bot.py
import os
import random

import datetime
from datetime import date
from datetime import datetime

import aiocron

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = int(os.getenv('DISCORD_GUILD'))

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

debug_mode = True

def get_online_members(members):
    result = []
    for member in members:
        if member.status in (discord.Status.online, discord.Status.idle) and client.user.id != member.id:
            result.append(member)

    return result

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="d-_-b"))

    guild = client.get_guild(GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name + " " + member.raw_status for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower() == "!radio":
        response = rollAndReturn()
        await message.channel.send(response)

    if "bocie" in message.content.lower():
        await message.channel.send("Co? Nie potrafię tego zrobić")
        
def checkIfSpecial(members):
    name = os.getenv('SPECIAL_NAME')
    special_date = datetime.strptime(os.getenv('SPECIAL_DATE'), '%d/%m/%y')
    if (date.today() == special_date.date()):
        for member in members:
            if name in member.name:
                print("It's a special day!")
                return member
            
    return None

def rollAndReturn():
    guild = client.get_guild(GUILD)

    person = checkIfSpecial(guild.members)
    if person == None:
        online_list = get_online_members(guild.members)
        person = random.choice(online_list)
        
    response = person.mention + " jest teraz DJem!"
    return response
            

@aiocron.crontab('0/10 8-20 * * MON,TUE,WED,THU,FRI')
async def regularRadio():
    channel_id = os.getenv('DEBUG_ID') if debug_mode else os.getenv('RADIO_ID')
    channel = client.get_channel(int(channel_id))
    response = rollAndReturn()
    await channel.send(response)


client.run(TOKEN)

