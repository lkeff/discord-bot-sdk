import discord
from discord.ext import commands
from localization.locales import Locales

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @discord.slash_command(
        name='ping',                             # default command name
        description='Default ping!',             # default command description
        **Locales().get_locales('ping-command')  # get translation for ru and en-GB locales
    )
    async def ping_command(self, ctx: discord.ApplicationContext):
        responses = {
            'default': 'Pong! Latency is',
            'ru': 'Понг! Задержка бота:',
            'en-gb': 'British pong! Latency is'
        }
        await ctx.respond(f'{Locales().locale_response(ctx.interaction, responses)} {str(round(self.bot.latency, 2))}')

def setup(bot):
    bot.add_cog(Ping(bot))