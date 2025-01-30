import json
import os
import inspect

from discord import ApplicationContext
from discord.interactions import Interaction

from utils.singleton import Singleton
from config import globals

def _(translations: dict[str, str], *formats: object) -> str:
    """Macros usage: _(Localization.greeting, ctx.user.name).
    Locale will be found from Interaction or CTX argument from parent functions."""
    frame = inspect.currentframe().f_back

    try:
        while frame:
            for value in frame.f_locals.values():
                if isinstance(value, (ApplicationContext, Interaction)):
                    return Locales().localize_string(value, translations, *formats)
            
            frame = frame.f_back
    except:
        pass

    # In case if we haven't found context - return first locale
    first_locale = next(iter(translations))
    return translations[first_locale].format(*formats) if formats else translations[first_locale]


class Locales(metaclass=Singleton):
    """Allows easily localize your commands and strings."""
    
    def __init__(self):
        with open(os.path.join(globals.ABS_PATH, 'localization', 'commands.json'), 'r', encoding='utf-8') as file:
            self.__commands: dict = json.load(file)

    def localize_command(self, name: str) -> dict:
        """Returns dict containing locales for current key"""
        return self.__commands.get(name, {})

    def localize_string(self, base_arg: Interaction | ApplicationContext, translations: dict[str, str], *formats: object) -> str:
        """Translates strings from dict with translations. Returns the base string if locale not exists in the dict"""
        ctx = base_arg if isinstance(base_arg, Interaction) else base_arg.interaction   

        if ctx.locale in translations:
            return translations[ctx.locale].format(*formats) if formats else translations[ctx.locale]
        else:
            first_locale = next(iter(translations))
            return translations[first_locale].format(*formats) if formats else translations[first_locale]
