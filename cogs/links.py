import discord
from discord.ext import commands
import sqlite3
bot = discord.Bot()
conn = sqlite3.connect("data/sobs.db")
cursor = conn.cursor()
class Links(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="links", description="Displays support links for SoBoard.")
    async def sobs(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="😭 Support SoBoard",
            color=discord.Colour.yellow()
        )
        embed.add_field(name="GitHub", value="[SoBoard Repository](https://github.com/sn-owy/SoBoard)", inline=False)
        embed.add_field(name="Ko-fi", value="[Support on Ko-fi](https://ko-fi.com/r00se)", inline=False)
        embed.add_field(name="Discord", value="[Join the Discord](https://discord.gg/rQGAp48cP2)", inline=False)
        embed.set_image(url="https://r2.e-z.host/a8d205e2-c05b-47a5-88de-e2b8c7916dbb/z1kjjgta.png")
        await ctx.respond(embed=embed, ephemeral=True)
def setup(bot: discord.Bot):
    bot.add_cog(Links(bot))
