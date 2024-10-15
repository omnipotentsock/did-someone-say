import discord
import random
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

token = os.environ["DISCORD_TOKEN"]
client = discord.Client(intents=intents)

response_list = {
    "hawk": [f'*hawk..?*', "hawk tuah! ~~spit on that thing~~ kill yourself!", "hawk? why don't you talk tuah some bitches?"],
    "crazy": ["crazy? i was crazy once. they locked me in a room. a rubber room. a rubber room with rats. and rats make me crazy.", "y'know what would be crazier tho? touching some grass"],
    "mn" : [f'MN mentioned!! what the fuck are "food options" rahhh!!'],
    "roll call": ["I am inside your walls"]
}

coin_flip = ["heads", "tails"]

@client.event
async def on_ready():
    print(f'{client.user} succesfully logged in!')

@client.event
async def on_message(message):
    # If it's the bot, return
    if message.author == client.user: 
        return

    if message.content.lower() == "heads or tails":
        t0 = random.randint(0, 1)
        res = coin_flip[t0]
        await message.channel.send(f'You landed a {res}!!', reference=message)
        return

    for word, responses in response_list.items():
        if word in message.content.lower():
            response = random.choice(responses)
            await message.channel.send(response, reference=message)
            return


client.run(token)