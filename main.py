import discord
import os 
from utils.utils import (LAVENDER)
#"Lavender lamborghini roll up in a new bikini bitches on the beaches looking super on and freaky" -Charli XCX on Vroom Vroom
from dotenv import load_dotenv
load_dotenv() 
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="sobs"))

#load commands
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("__"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv('TOKEN'))