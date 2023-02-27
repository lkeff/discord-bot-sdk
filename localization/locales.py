import json
from utils.singleton import Singleton
from discord.interactions import Interaction

class Locales(metaclass=Singleton):
    """
    @TODO: Create DOC string there
    """
    
    def __init__(self):
        with open('localization/locales.json', 'r') as file:
            self.__locales: dict = json.load(file)

    def get_locales(self, name: str) -> dict:
        """Returns dict containing locales for current key (if not exists returns empty dict)."""
        return self.__locales.get(name, {})
    
    def locale_response(self, intercation: Interaction, responses: dict):
        """Returns localed response from passed dictionary.
        If locale not in responses.keys(), you must define default key:value in dict.
        """
        return responses.get(intercation.locale, responses['default'] if 'default' in responses
                              else 'Please, define `default` key in dict')
