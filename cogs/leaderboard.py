import discord
from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="leaderboard", description="Users in the server with the highest amount of sobs")
    async def hello(self, ctx: discord.ApplicationContext):
        await ctx.respond("Hey!")
def setup(bot):
    bot.add_cog(Hello(bot))
