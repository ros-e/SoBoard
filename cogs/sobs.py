import discord
from discord.ext import commands
import sqlite3

bot = discord.Bot()

conn = sqlite3.connect("data/sobs.db")
cursor = conn.cursor()

class Sobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="sob_stats", description="Shows sob stats for a user.")
    async def sob_stats(self, ctx: discord.ApplicationContext, user: discord.User):
        user_id = str(user.id)
        
        cursor.execute("""
        SELECT SUM(sobs) FROM Users WHERE user_id = ?
        """, (user_id,))
        sobs_given = cursor.fetchone()[0]
        sobs_given = sobs_given if sobs_given else 0

        cursor.execute("""
        SELECT COUNT(*) FROM Users WHERE message_id IN (SELECT message_id FROM Users WHERE user_id = ?)
        """, (user_id,))
        sobs_received = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT COUNT(*) FROM Users WHERE user_id = ?
        """, (user_id,))
        sobworth = cursor.fetchone()[0]

        await ctx.respond(f"😭 {user.display_name}'s Sob Stats\n\nSobs Given: {sobs_given}\nSobs Received: {sobs_received}\nSobworth: {sobworth}")

def setup(bot):
    bot.add_cog(Sobs(bot))
