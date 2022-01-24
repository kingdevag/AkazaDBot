import discord
from discord.ext import commands
import keep_alive
import time
from discord_components import Button, DiscordComponents
import asyncio
import datetime
from urllib import parse, request
import re

token = "OTMzODYwNDczMDY4MTk1OTAw.YenrVw.lqdPF4IiMHxieBZ5wR4nCk8LT9w"
intents = discord.Intents.default()
intents.members = True
intents.guild_reactions = True
intents.guild_messages = True
intents.messages = True
Bot = commands.Bot(command_prefix='!', description="This is a Helper Bot")


#Commands

@Bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results=re.findall('watch\?v=(.{11})', html_content.read().decode('utf-8'))
    print(search_results)
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])
    
@Bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="my creator is ♞!i~𝞚ℝⱮ𝞓𝞟🅓𝞨;..♟#7094", timestamp=datetime.datetime.utcnow(), color=discord.Colour.blue())
    embed.add_field(name="Server create at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white")
    await ctx.send(embed=embed)

@Bot.command(pass_context=True)
async def help_bot(ctx):
  await ctx.send(
        "Que nesesitas?",
        components = [
            Button(label = "Comandos", custom_id = "boton1")
        ]
        
    )
  interaction = await Bot.wait_for("button_click", check = lambda i: i.custom_id == "boton1")
  embed = discord.Embed(title="Commands", description="!youtube \n !discord_nitro \n !hola \n !CM \n !m \n !info \n help", color=discord.Colour.blue())
  embed.set_thumbnail(url="https://i.pinimg.com/originals/c5/97/78/c59778757e58360f652399ece4b6c558.jpg")
  embed.set_footer(text=f"{ctx.user.name}")
  await interaction.send(embed=embed)

DiscordComponents(Bot)
 
@Bot.command(pass_context=True)
async def discord_nitro(ctx):
  await ctx.send(
        "JIJIJIJA",
        components = [
            Button(label = "apreta para discord nitro gratis", custom_id = "boton1")
        ]
    )
  interaction = await Bot.wait_for("button_click", check = lambda i: i.custom_id == "boton1")
  await interaction.send(content = "Never gonna give you up \n https://youtu.be/dQw4w9WgXcQ")

@Bot.command(pass_context=True)
async def hola(ctx):
    Mensage = ctx.message
    await ctx.send(f"Hola {Mensage.author.name}")
    
@Bot.command(pass_context=True)
async def m(ctx):
    Mensage = ctx.message
    await Mensage.delete()
    await ctx.send(Mensage.content)

@Bot.command(pass_context=True)
async def ping(ctx):
    antes = time.monotonic()
    mensage =    await ctx.send("Pong")
    ping1 = (time.monotonic() - antes)*1000
    ping2 =(str(ping1).split('.'))[0]
    await mensage.edit(content="pong! (" + ping2 + "ms)")
    
@Bot.command(pass_context=True)
async def stop_bot_131408(ctx):
   await ctx.send("Apagando Bot...")
   await Bot.close()
   
@Bot.command(pass_context=True)
async def CM(ctx, usuario:discord.Member, Nick):
    await usuario.edit(nick=Nick)
    

#events

@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Streaming(name="Python and Gaming", url="http://www.twitch.tv/k1ngag"))
    print(f"the bot {Bot.user} Ready")


#anti spam

async def silenciarUsuario(user, razon=".", temp=120):
    await user.add_roles(discord.utils.get(user.guild.roles, name="MUTE"))

    embedVar = discord.Embed(title=f"ESTÁS SILENCIADO", color=discord.Colour.red())
    embedVar.add_field(name=f"Razón: ", value=f"{razon}!", inline=True)
    embedVar.add_field(name=f"Duración silencio: ", value=f"{temp} segundos!", inline=True)
    embedVar.set_footer(text="No vuelvas a hacerlo o volverás a ser sancionado!")
    embedVar.set_thumbnail(url="https://i.ytimg.com/vi/9FlBtZiMCAw/hqdefault.jpg")

    await user.send(embed=embedVar)

    await asyncio.sleep(temp)
    await user.remove_roles(discord.utils.get(user.guild.roles, name="MUTE"))

cooldown = commands.CooldownMapping.from_cooldown(10, 10, commands.BucketType.member)
@Bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    if "MUTE" in str(msg.author.roles):
        await msg.delete()
        return
    retry_after = cooldown.update_rate_limit(msg)
    if retry_after:
        def check(msgb):
            return msgb.author.id == msg.author.id
        await msg.channel.purge(limit=10, check=check, before=None)
        await silenciarUsuario(msg.author, razon="Mandar muchos mensajes")
        return
    await Bot.process_commands(msg)

keep_alive.keep_alive()
Bot.run(token)