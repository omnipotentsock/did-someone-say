import aiohttp
import discord
from discord import app_commands
import random
import re
import os
from dotenv import load_dotenv

load_dotenv()

# message_content is the only privileged intent the bot actually uses for now im pretty sure
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

token = os.getenv("DISCORD_TOKEN")
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

SERVICE_URL = os.getenv("SERVICE_URL", "http://localhost:4000/graphql")

response_list = {
    "hawk": [
        "*hawk..?*",
        "hawk tuah! ~~spit on that thing~~",
        "hawk? why don't you talk tuah some grass?",
        "STOP RIGHT THERE.",
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
    await tree.sync()  # slash command registering
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
            "`/gengossipgirl`: pipes up and gossip girls. xoxo.\n"
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
        if re.search(rf"\b{re.escape(word)}\b", content):
            response = random.choice(responses)
            if random.randint(0, 100) < 20:
                response += TIP
            await message.channel.send(response, reference=message)
            return


# @tree.command(name="testicles", description="Does this work brehv")
# async def test_cmd(interaction: discord.Interaction):
#     await interaction.response.send_message("Hey yo! Radicall")


# GraphQL service gossip girl command
MUTATION = """
mutation ($names: [String!]!) {
    generateGossip(names: $names) { headline body signOff }
}
"""

async def fetch_gossip(names: list[str]) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            SERVICE_URL,
            json={"query": MUTATION, "variables": {"names": names}},
            timeout=aiohttp.ClientTimeout(total=30) # Might adjust timeout later depending on need
        ) as response:
            data = await response.json()
    if "errors" in data:
        # print(data["errors"][0][message])
        raise RuntimeError(data["errors"][0]["message"])
    g = data["data"]["generateGossip"]
    return f"**{g['headline']}**\n\n{g['body']}\n\n*{g['signOff']}*"

@tree.command(name="gengossipgirl", description="Spotted: gossip about your server")
async def gengossipgirl(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("Servers only, darling.", ephemeral=True)
        return
    await interaction.response.defer()  # cuz LLM calls exceed Discord's 3s limit

    humans = [m for m in interaction.guild.members if not m.bot]
    if len(humans) < 2:
        await interaction.followup.send("Not enough people to gossip about.")
        return

    picks = random.sample(humans, k=min(3, len(humans)))
    try:
        text = await fetch_gossip([m.display_name for m in picks])
    except Exception as e:
        print(f"gossip failed: {e}")
        await interaction.followup.send("The gossip mill is down. Try again later.")
        return
    await interaction.followup.send(text, allowed_mentions=discord.AllowedMentions.none())

client.run(token)