import discord
from discord.ext import commands
from localization.locales import Locales, _

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @discord.slash_command(
        name='ping',                             # default command name
        description='Default ping!',             # default command description
        **Locales().get_locales('ping_command')  # get ping_command name, description translation for ru and en-GB
    )
    async def ping_command(self, ctx: discord.ApplicationContext):
        await ctx.respond(_('Hello, my dear {}!', ctx.user.name) + f' {round(self.bot.latency, 2)}')

def setup(bot):
    bot.add_cog(Ping(bot))