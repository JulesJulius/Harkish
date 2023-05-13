import os
import discord
from dotenv import load_dotenv

load_dotenv()

from module_loader import ModuleLoader

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()

client = discord.Client(intents=intents)
module_loader = ModuleLoader(client)

@client.event
async def on_connect():
    print("client.event(on_connect)")
    
    await module_loader.on_connect()

@client.event
async def on_message(message):
    print("client.event(on_message)")
    
    await module_loader.on_message(message)

@client.event
async def on_ready():
    print("client.event(on_ready)")
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    await module_loader.on_ready()
    
client.run(TOKEN)
