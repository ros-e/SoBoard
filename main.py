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
    sobs_given INTEGER DEFAULT 0,
    sobs_received INTEGER DEFAULT 0,
    guild_id TEXT NOT NULL,
    PRIMARY KEY (user_id, guild_id),
    FOREIGN KEY (guild_id) REFERENCES Guilds(guild_id)
)
""")
conn.commit()

@bot.event
async def on_ready():
    await update_presence()
    print(f"{bot.user} is ready and online!")
@bot.event
async def on_guild_join(guild):
    await update_presence()
@bot.event
async def on_guild_remove(guild):
    await update_presence()
async def update_presence():
    server_count = len(bot.guilds)
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"sobs in {server_count} servers"
    ))

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if user.id == reaction.message.author.id:
        return
    
    if str(reaction.emoji) == "😭":
        guild_id = str(reaction.message.guild.id)
        user_id = str(user.id)  # user that reacted 
        message_author_id = str(reaction.message.author.id)  # message author
        
        cursor.execute("""
        INSERT INTO Guilds (guild_id)
        VALUES (?)
        ON CONFLICT(guild_id) DO NOTHING
        """, (guild_id,))
        
        cursor.execute("""
        INSERT INTO Users (user_id, sobs_given, sobs_received, guild_id)
        VALUES (?, 1, 0, ?)
        ON CONFLICT(user_id, guild_id) DO UPDATE SET
            sobs_given = sobs_given + 1
        """, (user_id, guild_id))
        
        cursor.execute("""
        INSERT INTO Users (user_id, sobs_given, sobs_received, guild_id)
        VALUES (?, 0, 1, ?)
        ON CONFLICT(user_id, guild_id) DO UPDATE SET
            sobs_received = sobs_received + 1
        """, (message_author_id, guild_id))
        
        conn.commit()

@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return
    
    if user.id == reaction.message.author.id:
        return
    
    if str(reaction.emoji) == "😭":
        guild_id = str(reaction.message.guild.id)
        user_id = str(user.id)  # user that reacted 
        message_author_id = str(reaction.message.author.id)  # message author
        
        cursor.execute("""
        UPDATE Users
        SET sobs_given = sobs_given - 1
        WHERE user_id = ? AND guild_id = ?
        """, (user_id, guild_id))
        
        cursor.execute("""
        UPDATE Users
        SET sobs_received = sobs_received - 1
        WHERE user_id = ? AND guild_id = ?
        """, (message_author_id, guild_id))
        
        conn.commit()


@bot.event
async def on_close():
    conn.close()
    print("Database connection closed.")
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("__"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv('TOKEN'))
