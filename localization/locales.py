import json
import os
import inspect

from discord import ApplicationContext
from discord.ext import commands
from discord.interactions import Interaction

from utils.singleton import Singleton
from config import globals


def _(string: str, *formats: object) -> str:
    """Macros usage: _("String").
    Locale will be found from Interaction or CTX argument from parent functions."""
    frame = inspect.currentframe().f_back

    try:
        while frame:
            cog: commands.Cog | None = None

            for value in frame.f_locals.values():
                if hasattr(value, '__class__') and issubclass(value.__class__, commands.Cog):
                    cog = value

                if isinstance(value, (ApplicationContext, Interaction)):
                    return Locales().localize_string(value, string, *formats, cog=cog)
            
            frame = frame.f_back
    except:
        pass

    return string.format(*formats) if formats else string


class Locales(metaclass=Singleton):
    """Allows easily localize your commands and strings."""
    
    def __init__(self):
        with open(os.path.join(globals.ABS_PATH, 'localization', 'commands.json'), 'r', encoding='utf-8') as file:
            self.__commands: dict = json.load(file)

        with open(os.path.join(globals.ABS_PATH, 'localization', 'strings.json'), 'r', encoding='utf-8') as file:
            self.__strings: dict = json.load(file)

    def localize_command(self, name: str) -> dict:
        """Returns dict containing locales for current key"""
        return self.__commands.get(name, {})

    def localize_string(self, base_arg: Interaction | ApplicationContext, string: str, *formats: object, cog: commands.Cog | None = None) -> str:
        """Translates only strings. If not exists returns the base string."""
        ctx = base_arg if isinstance(base_arg, Interaction) else base_arg.interaction   

        if cog and hasattr(cog, 'cog_locales'):
            localization = dict()
            localization.update(self.__strings)
            localization.update(cog.cog_locales)
        else:
            localization = self.__strings

        if string in localization:
            return_string = localization[string].get(ctx.locale, string)
            return return_string.format(*formats) if formats else return_string
        else:
            return string.format(*formats) if formats else string
