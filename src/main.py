import discord
from discord.ext import commands
import keep_alive
import time
from discord_components import *
import asyncio
import datetime
from urllib import parse, request
import re
import urllib.request
import json

token = "OTMzODYwNDczMDY4MTk1OTAw.YenrVw.lqdPF4IiMHxieBZ5wR4nCk8LT9w"
key = "AIzaSyAkBNWaoKYje04FdCZh_fKyzX8bGPwQACw"
intents = discord.Intents.default()
intents.members = True
intents.guild_reactions = True
intents.guild_messages = True
intents.messages = True
Bot = commands.Bot(command_prefix='!', description="This is a Helper Bot")


#Commands

@Bot.command()
async def invite(ctx):
    embed = discord.Embed(title=f"Click aqui para invitar a {Bot.user}", url='https://discord.com/api/oauth2/authorize?client_id=933860473068195900&permissions=8&scope=bot', desciption=".", color=discord.Colour.green())
    embed.set_author(name=Bot.user, icon_url=Bot.user.avatar_url)
    await ctx.send(embed=embed)
    
    
@Bot.command()
async def calc(ctx):
    m = await ctx.send(content='Cargando calculadora...')
    expression = 'None'
    delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    e = discord.Embed(title=f'{ctx.author.name}\'s Calculadora | {ctx.author.id}', description=expression,
                        timestamp=delta)
    await m.edit(components=buttons, embed=e)
    while m.created_at < delta:
        res = await client.wait_for('button_click')
        if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[
            0].timestamp < delta:
            expression = res.message.embeds[0].description
            if expression == 'None' or expression == 'A ocurrido un error':
                expression = ''
            if res.component.label == 'Exit':
                await res.respond(content='calculadora cerrada', type=7)
                break
            elif res.component.label == '←':
                expression = expression[:-1]
            elif res.component.label == 'Clear':
                expression = 'None'
            elif res.component.label == '=':
                expression = calculate(expression)
            else:
                expression += res.component.label
            f = discord.Embed(title=f'{res.author.name}\'s calculator|{res.author.id}', description=expression,
                                timestamp=delta)
            await res.respond(content='', embed=f, components=buttons, type=7)


@Bot.command()
async def user_info(ctx, user:discord.Member):
    embed = discord.Embed(title=f"{user.name}", description=f"Informacion de {user.name}", timestamp=datetime.datetime.utcnow(), color=discord.Colour.blue())
    embed.add_field(name="Rol:", value=f"{user.roles.name}")
    embed.add_field(name="Fecha de creacion:", value=f"{user.created_at}")
    await ctx.send(embed=embed)
    

@Bot.command(name='subs')
async def subscriptores(ctx,username):
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + username + "&key=" + key).read()
    subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    response = username + " tiene " + "{:,d}".format(int(subs)) + " suscriptores!"
    embed = discord.Embed(title=f"Subs de {username}:", description=f"{response}", color=discord.Colour.red())
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/YouTube_social_white_squircle.svg/2048px-YouTube_social_white_squircle.svg.png")
    await ctx.send(embed=embed)

@Bot.command()
async def sumar(ctx, num1,num2):
    response = int(num1)+int(num2)
    await ctx.send(response)

@Bot.command()
async def multiplicar(ctx, num1,num2):
    response = int(num1)*int(num2)
    await ctx.send(response)

@Bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results=re.findall('watch\?v=(.{11})', html_content.read().decode('utf-8'))
    print(search_results)
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])
    
@Bot.command()
async def server_info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="my creator is ♞!i~𝞚ℝⱮ𝞓𝞟🅓𝞨;..♟#7094", timestamp=datetime.datetime.utcnow(), color=discord.Colour.blue())
    embed.add_field(name="Server create at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white")
    await ctx.send(embed=embed)
    
 
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
async def secret( ctx, *, arg):
    Mensage = ctx.message
    await Mensage.delete()
    await ctx.send(arg)

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
async def name_edit(ctx, usuario:discord.Member, Nick):
    await usuario.edit(nick=Nick)
    

#events

@Bot.event
async def on_command_error(ctx, error):
    await ctx.send("Ingresa un comando valido")


@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Streaming(name="Python and Gaming", url="http://www.twitch.tv/k1ngag"))
    print("+===============================+")
    print(f"the bot {Bot.user} Ready")
    print(f"ID: {Bot.user.id}")
    print("+===============================+")
    
    
    DiscordComponents(Bot)
 
buttons = [
    [
        Button(style=ButtonStyle.grey, label='1'),
        Button(style=ButtonStyle.grey, label='2'),
        Button(style=ButtonStyle.grey, label='3'),
        Button(style=ButtonStyle.blue, label='×'),
        Button(style=ButtonStyle.red, label='Exit')
    ],
    [
        Button(style=ButtonStyle.grey, label='4'),
        Button(style=ButtonStyle.grey, label='5'),
        Button(style=ButtonStyle.grey, label='6'),
        Button(style=ButtonStyle.blue, label='÷'),
        Button(style=ButtonStyle.red, label='←')
    ],
    [
        Button(style=ButtonStyle.grey, label='7'),
        Button(style=ButtonStyle.grey, label='8'),
        Button(style=ButtonStyle.grey, label='9'),
        Button(style=ButtonStyle.blue, label='+'),
        Button(style=ButtonStyle.red, label='Clear')
    ],
    [
        Button(style=ButtonStyle.grey, label='00'),
        Button(style=ButtonStyle.grey, label='0'),
        Button(style=ButtonStyle.grey, label='.'),
        Button(style=ButtonStyle.blue, label='-'),
        Button(style=ButtonStyle.green, label='=')
    ],
]
 
def calculate(exp):
    o = exp.replace('×', '*')
    o = o.replace('÷', '/')
    result = ''
    try:
        result = str(eval(o))
    except:
        result = 'A ocurrido un error'
    return result


#Help_bot

@Bot.command()
async def help_bot(ctx):
    comandos = "Prefijo del bot: \n ! o /  "
    embed = discord.Embed(title=Bot.user, url='https://discord.com/api/oauth2/authorize?client_id=933860473068195900&permissions=8&scope=bot', desciption=comandos, color=discord.Colour.blue())
    embed.add_field(name="Comandos: \n   help", value="Sirve para pedir ayuda sobre el bot \n Ya sea sobre comandos, informacion o funciones.")
    embed.add_field(name="name_edit", value=f"Cambia el nombre del etiquetado, ejemplo: !name_edit @{Bot.user}")
    embed.add_field(name="secret", value="Manda un mensaje sin nombre del autor")
    embed.add_field(name="discord_nitro", value="Pruebalo...")
    embed.add_field(name="hola", value="Saludas al bot")
    embed.add_field(name="server_info", value=f"Proporciona informacion sobre el servidor {ctx.guild.name}")
    embed.add_field(name="subs", value="Proporciona el numero de subscriptores, Ejemplo: !subs HolaSoyGerman")
    embed.add_field(name="youtube", value="Funciona como un buscador de youtube")
    embed.add_field(name="sumar", value="Suma 2 numeros diferentes")
    embed.add_field(name="multiplicar", value="Multiplica 2 numeros diferentes")
    embed.add_field(name="calc", value="Crea una calculadora con botones")
    embed.add_field(name="user_info", value="Proporciona informacion sobre un usuario")
    embed.add_field(name="invite", value=f"Con el puedes invitar a {Bot.user} en otro servidor")
    embed.set_author(name=Bot.user, icon_url=Bot.user.avatar_url)
    embed.set_thumbnail(url=Bot.user.avatar_url)
    await ctx.send(embed=embed)


#Anti spam

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