import discord
import os
from dotenv import load_dotenv
import sqlite3
from utils.utils import intents

load_dotenv()
bot = discord.Bot(intents=intents)

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/sobs.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Guilds (
    guild_id TEXT PRIMARY KEY
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    user_id TEXT NOT NULL,
    display_name TEXT NOT NULL,
    message TEXT NOT NULL,
    sobs INTEGER DEFAULT 0,
    message_id TEXT NOT NULL,
    guild_id TEXT NOT NULL,
    PRIMARY KEY (user_id, message_id),
    FOREIGN KEY (guild_id) REFERENCES Guilds(guild_id)
)
""")
conn.commit()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="sobs"))

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if str(reaction.emoji) == "😭":
        guild_id = str(reaction.message.guild.id)
        user_id = str(user.id)
        display_name = str(user.display_name)
        message_content = str(reaction.message.content)
        message_id = str(reaction.message.id)

        cursor.execute("""
        INSERT INTO Guilds (guild_id)
        VALUES (?)
        ON CONFLICT(guild_id) DO NOTHING
        """, (guild_id,))

        cursor.execute("""
        INSERT INTO Users (user_id, display_name, message, sobs, message_id, guild_id)
        VALUES (?, ?, ?, 1, ?, ?)
        ON CONFLICT(user_id, message_id) DO UPDATE SET
            sobs = sobs + 1
        """, (user_id, display_name, message_content, message_id, guild_id))

        conn.commit()

@bot.event
async def on_close():
    conn.close()
    print("Database connection closed.")

#load commands
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("__"):
        bot.load_extension(f"cogs.{filename[:-3]}")


    
bot.run(os.getenv('TOKEN'))
