import discord
from discord.ext import commands


class EventsManager(commands.Cog):
    """Here can be stored events that not linked to any Cog."""

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        import logging
        from utils.redact import redact_sensitive
        logging.basicConfig(level=logging.INFO)
        logging.info(redact_sensitive(f"{self.bot.user} is ready and online!"))
    

def setup(bot):
    bot.add_cog(EventsManager(bot))