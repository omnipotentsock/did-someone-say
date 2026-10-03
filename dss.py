import discord
from discord import app_commands
import random
import re
import os
from dotenv import load_dotenv

load_dotenv()

# message_content is the only privileged intent the bot actually uses
intents = discord.Intents.default()
intents.message_content = True

token = os.getenv("DISCORD_TOKEN")
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

response_list = {
    "hawk": [
        "*hawk..?*",
        "hawk tuah! ~~spit on that thing~~ NO STOP",
        "hawk? why don't you talk tuah some grass?",
    ],
    "crazy": [
        "crazy? i was crazy once. they locked me in a room. a rubber room. a rubber room with rats. and rats make me crazy.",
        "y'know what would be crazier tho? touching some grass",
    ],
    "mn": ['MN mentioned!! what the hell are "food options" rahhh!!'],
}

coin_flip = ["heads", "tails"]
TIP = "\n\n*Tip: type `dss wyd` to get a list of commands and features*"


@client.event
async def on_ready():
    await tree.sync()  # registers slash commands with Discord
    print(f"{client.user} successfully logged in!")


@client.event
async def on_message(message):
    # If it's the bot, return
    if message.author == client.user:
        return

    content = message.content.lower()

    if content == "dss wyd":
        await message.channel.send(
            "I'm chilling! Here are all the things I can do. \n\n"
            "**Features:**\n"
            "`dss wyd`: prints this message \n"
            "`dss triggers`: get a list of words that trigger a response\n"
            "`heads or tails`: flips a coin and gives the result\n"
            "\n*for any further help, issues, or feature requests, message @adoopted*",
            reference=message,
        )
        return

    if content == "dss triggers":
        reply = "**Here are all the trigger words I will reply to:**"
        for word in response_list:
            reply += "\n" + word
        await message.channel.send(reply, reference=message)
        return

    if content == "heads or tails":
        res = random.choice(coin_flip)
        await message.channel.send(f"You landed a {res}!!", reference=message)
        return

    for word, responses in response_list.items():
        # \b word boundaries so "hawk?" or "crazy!!" still match
        if re.search(rf"\b{re.escape(word)}\b", content):
            response = random.choice(responses)
            if random.randint(0, 100) < 20:
                response += TIP
            await message.channel.send(response, reference=message)
            return


# @tree.command(name="testicles", description="Does this work brehv")
# async def test_cmd(interaction: discord.Interaction):
#     await interaction.response.send_message("Hey yo! Radicall")


client.run(token)