import nextcord
from nextcord.ext import commands

class funcommands(commands.Cog, name="Diversion"):
    """Comandos Divertidos"""
    COG_EMOJI = "🤡"
    
    def __init__(self, Bot):
        self.Bot = Bot 