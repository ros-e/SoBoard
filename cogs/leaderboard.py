import discord
from discord.ext import commands
import sqlite3

bot = discord.Bot()
conn = sqlite3.connect("data/sobs.db")
cursor = conn.cursor()
class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="leaderboard", description="View the server's sob leaderboard.")
    async def leaderboard(self, ctx: discord.ApplicationContext):
        guild_id = str(ctx.guild.id)
        cursor.execute("""
        SELECT user_id, sobs_received
        FROM Users
        WHERE guild_id = ?
        ORDER BY sobs_received DESC
        LIMIT 10
        """, (guild_id,))
        leaderboard_data = cursor.fetchall()
        if not leaderboard_data:
            await ctx.respond(embed=discord.Embed(
                title="😭 Sob Leaderboard",
                description="No sob stats found for this server.",
                color=discord.Colour.red()
            ))
            return
        leaderboard_entries = [
            f"**{idx + 1}.** <@{user_id}> — **{sobs}** sobs"
            for idx, (user_id, sobs) in enumerate(leaderboard_data)
        ]
        leaderboard_string = "\n".join(leaderboard_entries)
        embed = discord.Embed(
            title=f"😭 **{ctx.guild.name}'s Sob Leaderboard**",
            description=leaderboard_string,
            color=discord.Colour.yellow()
        )
        embed.set_footer(text="Support me on GitHub /links")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Leaderboard(bot))
