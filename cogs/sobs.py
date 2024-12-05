import discord
from discord.ext import commands
import sqlite3
from utils.utils import(YELLOW)

bot = discord.Bot()

conn = sqlite3.connect("data/sobs.db")
cursor = conn.cursor()

class Sobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="sobs", description="Shows sob stats for a user.")
    async def sobs(self, ctx: discord.ApplicationContext, user: discord.User):
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
        embed = discord.Embed(
            title=(f"😭 **{user.display_name}'s Sob Stats**\n\n"),
            color=discord.Colour.yellow()
        )
        embed.add_field(name="Sobs Received", value=sobs_received, inline=False)
        embed.add_field(name="Sobs Given", value=sobs_given, inline=False)
        embed.set_footer(text=f"support me on Github /links")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Sobs(bot))
