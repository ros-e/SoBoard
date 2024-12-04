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
        SELECT sobs_given FROM Users WHERE user_id = ? AND guild_id = ?
        """, (user_id, str(ctx.guild.id)))
        result = cursor.fetchone()
        sobs_given = result[0] if result else 0
        cursor.execute("""
        SELECT SUM(sobs_received) FROM Users WHERE user_id = ? AND guild_id = ?
        """, (user_id, str(ctx.guild.id)))
        sobs_received = cursor.fetchone()[0]
        sobs_received = sobs_received if sobs_received else 0

        sobworth = sobs_given + sobs_received 
        await ctx.respond(f"😭 **{user.display_name}'s Sob Stats**\n\n"
                          f"Sobs Given: {sobs_given}\n"
                          f"Sobs Received: {sobs_received}\n"
                          f"Sobworth: {sobworth}")

def setup(bot):
    bot.add_cog(Sobs(bot))
