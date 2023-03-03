import json
import os
import inspect
from discord import ApplicationContext
from discord.interactions import Interaction
from utils.singleton import Singleton
from config import globals

# Macros to localize strings
def _(string: str, *formats: object) -> str:
    """Main idea is to find the Interaction or CTX argument from parent function."""
    try:
        for value in inspect.currentframe().f_back.f_locals.values():
            if isinstance(value, (ApplicationContext, Interaction)):
                return Locales().localize_string(value, string, *formats)

        for value in inspect.currentframe().f_back.f_back.f_locals.values():
            if isinstance(value, (ApplicationContext, Interaction)):
                return Locales().localize_string(value, string, *formats)
    except:
        pass

    return string.format(*formats) if formats else string


class Locales(metaclass=Singleton):
    """Allows easily localize your commands and strings."""
    
    def __init__(self):
        with open(os.path.join(globals.ABS_PATH, 'localization', 'locales.json'), 'r', encoding='utf-8') as file:
            self.__locales: dict = json.load(file)

    def get_locales(self, name: str) -> dict:
        """Returns dict containing locales for current key (if not exists returns empty dict)."""
        return self.__locales.get(name, {})

    def localize_string(self, base_arg: Interaction | ApplicationContext, string: str, *formats: object) -> str:
        """Translates only strings. If not exists returns the base string."""
        loacle = base_arg.locale if isinstance(base_arg, Interaction) else base_arg.interaction.locale

        if string in self.__locales["strings"]:
            return_string = self.__locales["strings"][string].get(loacle, string)
            return return_string.format(*formats) if formats else string
        else:
            return string.format(*formats) if formats else string
