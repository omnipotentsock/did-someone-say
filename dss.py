
import discord
from discord_token import TOKEN

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} succesfully logged in!')

@client.event
async def on_message(message):
    # If it's the bot, return
    if message.author == client.user: 
        return
    
    if message.content == 'hello':
        await message.channel.send(f'Sup {message.author}')


client.run(TOKEN)