import nextcord
from nextcord.ext import commands

class funcommands(commands.Cog, name="Diversion"):
    """Comandos Divertidos"""
    COG_EMOJI = "🤡"
    
    def __init__(self, Bot):
        self.Bot = Bot 
    @commands.command(pass_context=True)
    async def secret( ctx, *, arg):
        """Envia un mensaje sin Author"""
        Mensage = ctx.message
        await Mensage.delete()
        await ctx.send(arg)
        
    @commands.command(pass_context=True)
    async def name_edit(ctx, usuario:nextcord.Member, Nick):
        """Cambia el nombre del usuario Mencionado"""
        await usuario.edit(nick=Nick)