import discord
from io import BytesIO
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from discord import File
from loguru import logger
import json
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("token")
logger.add("Logs.log")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


def get_config() -> dict:
    with open("config.json", "r") as f:
            jdata = json.load(f)
    return  jdata

@bot.event
@logger.catch
async def on_ready():
    print("Bot is up and ready!")

    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command[s]")
    except Exception as e:
        logger.error(str(e))


def create_embed(
    title: str, content: str, color: discord.Color
):  # easily create an embed
    embed = discord.Embed(title=title, color=color)
    embed.add_field(name=content, value="")
    return embed

@bot.tree.command(name="configurate")
async def configurate(interaction:discord.Interaction,image_url:str,channels:str):
    await interaction.response.defer()
    channels:list = [channel.removeprefix('<#').removesuffix('>') for channel in channels.split(' ')]
    for channel in channels:
        try:
            channels.remove("")
        except:
            pass
    print(channels)
    Config = {
         "image_url":image_url,
         "channels":list(channels)
    }
    with open("config.json", "w") as f:
        json.dump(Config, f)

    embed = create_embed("Success", "Configured Succesfully", discord.Color.green())
    await interaction.followup.send(embed=embed)

@bot.event
async def on_message(message:discord.Message):
    print([channel for channel in list(get_config()["channels"])])
    if message.channel.id in list([int(channel) for channel in list(get_config()["channels"])]) and message.author.id != bot.user.id:
        await message.channel.send(get_config()["image_url"])
    else:
        pass


bot.run(token=TOKEN)
