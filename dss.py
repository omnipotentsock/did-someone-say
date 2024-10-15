import discord
import random
import os

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

token = os.environ["DISCORD_TOKEN"]
client = discord.Client(intents=intents)

response_list = {
    "hawk": [f'*hawk..?*', "hawk tuah! ~~spit on that thing~~ kill yourself!", "hawk? why don't you talk tuah some bitches?"],
    "crazy": ["crazy? i was crazy once. they locked me in a room. a rubber room. a rubber room with rats. and rats make me crazy.", "y'know what would be crazier tho? touching some grass"],
    "mn" : [f'MN mentioned!! what the fuck are "food options" rahhh!!']
}

@client.event
async def on_ready():
    print(f'{client.user} succesfully logged in!')

@client.event
async def on_message(message):
    # If it's the bot, return
    if message.author == client.user: 
        return
    
    if "hawk" in message.content:
        await message.channel.send(f'*`did someone say..?`*', reference=message)

    for word, responses in response_list.items():
        if word in message.content.lower():
            response = random.choice(responses)
            await message.channel.send(response, reference=message)
            return


client.run(token)