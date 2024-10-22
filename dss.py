import discord
from discord import app_commands
import random
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True


token = os.getenv("DISCORD_TOKEN")
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

response_list = {
    "hawk": [f'*hawk..?*', "hawk tuah! ~~spit on that thing~~ kill yourself!", "hawk? why don't you talk tuah some bitches?"],
    "crazy": ["crazy? i was crazy once. they locked me in a room. a rubber room. a rubber room with rats. and rats make me crazy.", "y'know what would be crazier tho? touching some grass"],
    "mn" : [f'MN mentioned!! what the fuck are "food options" rahhh!!']
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

    if message.content.lower() == "dss wyd":
        await message.channel.send(
            "I'm chilling! Here are all the things I can do. \n\n" +
            "**Features:**\n" +
            "`dss wyd`: prints this message \n" +
            "`dss triggers`: get a list of words that trigger a response\n" +
            "`heads or tails`: flips a coin and gives the result\n" +
            "`blackjack me off`: starts a game of blackjack *(currently under development)*\n" +
            "\n*for any further help, issues, or feature requests, message @adoopted*", 
            reference=message
        )

    if message.content == "dss triggers":
        reply = "**Here are all the trigger words I will reply to:**"
        for word in response_list.keys():
            reply += "\n" + word
        await message.channel.send(reply, reference=message)
        return

    if message.content.lower() == "heads or tails":
        t0 = random.randint(0, 1)
        res = coin_flip[t0]
        await message.channel.send(f'You landed a {res}!!', reference=message)
        return

    if message.content.lower() == 'blackjack me off':
        await message.channel.send(f'This feature is not ready yet! Try again later.')

    for word, responses in response_list.items():
        if word in message.content.lower().split():
            response = random.choice(responses)

            t0 = random.randint(0,100)
            if t0 < 20:
                await message.channel.send(response + "\n\n*Tip: type `dss wyd` to get a list of commands and features*", reference=message)
                return
            await message.channel.send(response, reference=message)
            return

@tree.command(
    name="testicles",
    description="Does this work brehv"
)
async def TestCmd(interaction):
    await message.channel.send(f'Hey yo! Radicall')


client.run(token)