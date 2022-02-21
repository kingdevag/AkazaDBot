#Imports
import nextcord
import os
import keep_alive
import asyncio
import datetime
import re
import urllib.request
import json
import random
import aiosqlite

#From-Import
from nextcord.ext import commands
from nextcord import *
from dotenv import load_dotenv
from urllib import parse, request
from colorama import Fore
from colorama import Style

#CogsImports
from modules.music import Player
from modules.help import *
from modules.funcommands import funcommands

load_dotenv()

host =os.environ['host']
token = os.environ['token']
key = os.environ['key']
version = os.environ['version']
spassword = os.environ['password']

intents = nextcord.Intents.default()
intents.members = True
intents.guild_reactions = True
intents.guild_messages = True
intents.messages = True

def get_prefix(Bot, message):
    with open('json/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
        return prefixes[str(message.guild.id)]

Bot = commands.Bot(command_prefix = get_prefix, intents=intents, description="Default prefix: !")

Bot.author_id = 681903559175962687

#CustomPrefix

@Bot.event
async def on_guild_join(guild):
    with open('json/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    prefixes[str(guild.id)] = '!'
    
    with open('json/prefixes.json', 'w')as f:
        
        json.dump(prefixes, f, indent=4)
        
@Bot.event
async def on_guild_remove(guild):
    with open('json/prefixes.json', 'r+') as f:
        prefixes = json.load(f)
        
        prefixes.pop(str(guild.id))
    
        with open('json/prefixes.json', 'w')as f:
            json.dump(prefixes, f)
    

@Bot.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix):
    with open('json/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    prefixes[str(ctx.guild.id)] = prefix
    
    with open('json/prefixes.json', 'w')as f:
        json.dump(prefixes, f)
    await ctx.send(f'El nuevo prefijo es {prefix}')
    pree = prefix
        

        

#Extras

@Bot.remove_command('help')

#Commands

@Bot.command()
async def reload(ctx, Bot: commands.Bot, arg):
    auid = "681903559175962687"
    if message.author.id is auid:
        Bot.reload_extension(arg)
        await ctx.send(f"{arg} Se a recargado correctamente")
        
    if arg is None:
        await ctx.send("Debes ingresar un Cog")

@Bot.command()
async def user_info(ctx, *, member: nextcord.Member):
    embed = nextcord.Embed(title=f"Informacion sobre {member}", color=nextcord.Color.blue())
    embed.add_field(name="Nombre", value=member.name)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Se creo el", value=member.created_at)
    embed.add_field(name="Se unio el", value=member.joined_at)
    
    await ctx.send(embed=embed)


@Bot.command()
async def web(ctx):
    await ctx.send("https://bot.k1ngdev-server.repl.co")

@Bot.command()
async def bot_info(ctx):
    embed = nextcord.Embed(title=f"Informacion sobre {Bot.user}", url='https://discord.com/api/oauth2/authorize?client_id=933860473068195900&permissions=8&scope=bot', description=f"Informacion sobre el Bot {Bot.user.name}", color=nextcord.Color.green())
    embed.add_field(name="Nombre", value=f"{Bot.user.name}")
    embed.add_field(name="Bot creado por", value="♞!i~𝞚ℝⱮ𝞓𝞟🅓𝞨;..♟#7094")
    embed.add_field(name="ID Del Bot", value=f"{Bot.user.id}")
    embed.add_field(name="Version del Bot", value=f"{version}")
    embed.add_field(name="Ping del Bot", value=f'{round (Bot.latency * 1000)}ms')
    embed.set_footer(text=f"{ctx.message.author.name} Esperamos que te aya servido esta informacion")
    embed.set_thumbnail(url=Bot.user.avatar)
    embed.set_author(name=Bot.user, icon_url=Bot.user.avatar  )
    
    await ctx.send(embed=embed)

@Bot.command()
async def invite(ctx):
    embed = nextcord.Embed(title=f"Click aqui para invitar a {Bot.user}", url='https://discord.com/api/oauth2/authorize?client_id=933860473068195900&permissions=8&scope=bot', desciption=".", color=nextcord.Colour.green())
    embed.set_author(name=Bot.user, icon_url=Bot.user.avatar)
    embed.set_footer(text=f"{ctx.message.author.name}Agrega a {Bot.user.name} a tu servidor :)")
    embed.set_thumbnail(url=ctx.message.author.avatar)
    await ctx.send(embed=embed)


@Bot.command(name='subs')
async def subscriptores(ctx,username):
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + username + "&key=" + key).read()
    subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    response = username + " tiene " + "{:,d}".format(int(subs)) + " suscriptores!"
    embed = nextcord.Embed(title=f"Subs de {username}:", description=f"{response}", color=nextcord.Colour.red())
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/YouTube_social_white_squircle.svg/2048px-YouTube_social_white_squircle.svg.png")
    await ctx.send(embed=embed)


@Bot.command()
async def sumar(ctx, num1,num2):
    response = int(num1)+int(num2)
    embed = nextcord.Embed(title="Respuesta", description=f"{num1} + {num2} = {response}", color=nextcord.Color.green())
    await ctx.send(embed=embed)


@Bot.command()
async def multiplicar(ctx, num1,num2):
    response = int(num1)*int(num2)
    embed = nextcord.Embed(title="Respuesta", description=f"{num1} X {num2} = {response}", color=nextcord.Color.green())
    await ctx.send(embed=embed)
    
    
@Bot.command()
async def dividir(ctx, num1,num2):
    response = int(num1)/int(num2)
    embed = nextcord.Embed(title="Respuesta", description=f"{num1} ÷ {num2} = {response}", color=nextcord.Color.green())
    await ctx.send(embed=embed)


@Bot.command()
async def restar(ctx, num1,num2):
    response = int(num1)-int(num2)
    embed = nextcord.Embed(title="Respuesta", description=f"{num1} - {num2} = {response}", color=nextcord.Color.green())
    await ctx.send(embed=embed)


@Bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results=re.findall('watch\?v=(.{11})', html_content.read().decode('utf-8'))
    print(search_results)
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])
    
    
@Bot.command()
async def server_info(ctx):
    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in  ctx.guild.members if bot.bot]
    
    embed = nextcord.Embed(title=f"{ctx.guild.name} Server Info", description="Server info", timestamp=datetime.datetime.utcnow(), color=nextcord.Colour.blue())
    embed.add_field(name="Nombre", value=f"{ctx.guild.name}")
    embed.add_field(name="Descripcion", value=f"{ctx.guild.description}")
    embed.add_field(name="Servidor creado el", value=f"{ctx.guild.created_at}")
    embed.add_field(name="nivel de verificación", value=str(ctx.guild.verification_level))
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Rol mas alto", value=ctx.guild.roles[-2])
    embed.add_field(name="Bots", value=', '.join(list_of_bots))
    embed.add_field(name="Numero de miembros", value=f"{ctx.guild.member_count}")
    embed.add_field(name="Numero de roles", value=str(role_count))
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
    embed.set_thumbnail(url=ctx.guild.icon)
    await ctx.send(embed=embed)
    


@Bot.command(pass_context=True)
async def hola(ctx):
    Mensage = ctx.message
    await ctx.send(f"Hola {Mensage.author.mention}")
    
    
@Bot.command(pass_context=True)
async def console(ctx, arg:str):
    print(arg)
 
@Bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def stop(ctx, password):
    if(ctx.message.author.id == "681903559175962687"):
        if(password == spassword):
            await ctx.send("Apagando Bot...")
            await Bot.close()
        if(password != spassword):
            await ctx.send("Password Incorrecto")
@stop.error
async def stop(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Ingresa una Password")
    

#SysCommands


@Bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f'Pong! ({round (Bot.latency * 1000)}ms)')
    

@Bot.command(pass_context=True)
async def save(ctx, save:str):
    save = ' '.join(save)
    with open('json/database.json', "r+") as f:
        database = json.load(f)
    database[str(ctx.author.id)] = str(save)
    with open('json/database.json', "r+") as f:
        json.dump(database, f)
    await ctx.send("Texto Guardado en Database.json")
    

#events

@Bot.event
async def on_ready():
    async with aiosqlite.connect('server/server.db') as db:
        async with db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS welcome (channel_text ID, guild ID)')
        await db.commit()

        
    await Bot.change_presence(activity=nextcord.Game(name="Utiliza !help",))
    print(Fore.WHITE + "+===============================+" + Style.RESET_ALL)
    print(Fore.GREEN + "---BOT ONLINE---" + Style.RESET_ALL)
    print(f"{Fore.GREEN} The Bot {Bot.user} Ready {Style.RESET_ALL}")
    print(f"{Fore.WHITE} Bot Version {version} {Style.RESET_ALL}")
    print(f"{Fore.WHITE} ID: {Bot.user.id} {Style.RESET_ALL}")
    print(f"{Fore.CYAN} Open Server.db = True {Style.RESET_ALL}")
    print(f"{Fore.YELLOW} Open databases.json = True {Style.RESET_ALL}") 
    print(Fore.WHITE + "+===============================+" + Style.RESET_ALL)
    

#Bienvenidas

@Bot.event
async def on_member_join(member):
    async with aiosqlite.connect('server/server.db') as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT channel_text FROM welcome WHERE guild = ?', (member.guild.id,))
            data = await cursor.fetchone()
            if data:
                channel_text = int(data[0])
                if channel_text == 0:
                    pass
                else:
                    try:
                        channel_text = await Bot.fetch_channel(channel_text)
                        embed = nextcord.Embed(title=f"{member.name} Bienvenid@ a {member.guild.name}", description="", color=nextcord.Color.green())
                        embed.set_author(name=Bot.user, icon_url=Bot.user.avatar)
                        embed.set_thumbnail(url=member.avatar)
                        await channel_text.send(embed=embed)
                    except:
                        pass
            else:
                pass
        await db.commit()

@Bot.command(name='configbienvenida')
async def bienvenidac(ctx, canal=None):
    if not canal:
        async with aiosqlite.connect('server/server.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute('SELECT channel_text FROM welcome WHERE guild = ?', (ctx.guild.id,))
                data = await cursor.fetchone()
                if  data:
                    await cursor.execute('UPDATE welcome SET channel_text = ? WHERE guild = ?', (0, ctx.guild.id,))
                else:
                    await cursor.execute('INSERT INTO welcome (channel_text, guild) VALUES (?, ?)', (0, ctx.guild.id,))
            await db.commit()
        return await ctx.send('Canal de texto eliminado con exito!')
    
    if re.findall('^<#([0-9]+)>$', canal):
        canal = re.findall('^<#([0-9]+)>$', canal)
        canal = canal[0]
    try:
        canal = int(canal)
    except:
        return await ctx.send('El ID no es valido')
    async with aiosqlite.connect('server/server.db') as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT channel_text FROM welcome WHERE guild = ?', (ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute('UPDATE welcome SET channel_text = ? WHERE guild = ?', (canal, ctx.guild.id,))
            else:
                await cursor.execute('INSERT INTO welcome (channel_text, guild) VALUES (?, ?)', (canal, ctx.guild.id,))
        await db.commit()
    await ctx.send('El canal de texto a sido guardado con exito!')
    

#AutoRole

@Bot.event
async def on_member_join(ctx):
    role = nextcord.utils.get(ctx.guild.roles, name = 'nuevo')
    await ctx.add_roles(role)


#MiniGames

jugador = ""
jugador2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@Bot.command()
async def game(ctx, p1: nextcord.Member, p2: nextcord.Member):
    global count
    global jugador
    global jugador2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        jugador2 = p2
        jugador = p1

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = jugador
            await ctx.send("It is <@" + str(jugador.id) + ">Tu turno.")
        elif num == 2:
            turn = jugador2
            await ctx.send("<@" + str(jugador2.id) + ">Tu turno.")
    else:
        await ctx.send("¡Ya hay un juego en progreso! Termínalo antes de empezar uno nuevo.")

@Bot.command()
async def lugar(ctx, pos: int):
    global turn
    global jugador
    global jugador2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == jugador:
                mark = ":regional_indicator_x:"
            elif turn == jugador2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " Gano!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("¡Es un empate!")

                # switch turns
                if turn == jugador:
                    turn = jugador2
                elif turn == jugador2:
                    turn = jugador
            else:
                await ctx.send("Asegúrese de elegir un número entero entre 1 y 9 y un mosaico sin marcar.")
        else:
            await ctx.send("no es tu turno.")
    else:
        await ctx.send("Inicie un nuevo juego usando el comando: !game")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


#Anti spam

async def silenciarUsuario(user, razon=".", temp=120):
    await user.add_roles(nextcord.utils.get(user.guild.roles, name="MUTE"))

    embedVar = nextcord.Embed(title=f"ESTÁS SILENCIADO", color=nextcord.Colour.red())
    embedVar.add_field(name=f"Razón: ", value=f"{razon}!", inline=True)
    embedVar.add_field(name=f"Duración silencio: ", value=f"{temp} segundos!", inline=True)
    embedVar.set_footer(text="No vuelvas a hacerlo o volverás a ser sancionado!")
    embedVar.set_thumbnail(url="https://i.ytimg.com/vi/9FlBtZiMCAw/hqdefault.jpg")

    await user.send(embed=embedVar)

    await asyncio.sleep(temp)
    await user.remove_roles(nextcord.utils.get(user.guild.roles, name="MUTE"))

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


#Errors




@subscriptores.error
async def subscriptores(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=nextcord.Embed(title="Error", description="Ingresa el nombre del Youtuber, Recuerda que solo funciona con Youtubers Verificados", color=nextcord.Color.red())
        embed.set_author(name=f"{Bot.user.name}", icon_url=f"{Bot.user.avatar_url}")
        await ctx.send(embed=embed)
        
    
@game.error
async def game(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        embed=nextcord.Embed(title="Error", description="Mencione 2 jugadores para este comando.", color=nextcord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed1=nextcord.Embed(title="Error", description="Por favor asegúrate de mencionar / hacer ping a los jugadores.", color=nextcord.Color.red())
        await ctx.send(embed=embed1)

@lugar.error
async def lugar(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=nextcord.Embed(title="Error", description="Ingrese una posición que le gustaría marcar.", color=nextcord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed1=nextcord.Embed(title="Error", description="Por favor asegúrese de ingresar un número entero.", color=nextcord.Color.red())
        await ctx.send(embed=embed1)


@prefix.error
async def prefix(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=nextcord.Embed(title="Error", description="Ingrese un prefijo", color=nextcord.Color.red())
        await ctx.send(embed=embed)
        
     

#Cogs

async def setup(Bot: commands.Bot):
    await Bot.wait_until_ready()
    Bot.add_cog(Player(Bot))
    
def funfuntion(Bot: commands.Bot):
    Bot.add_cog(funcommands(Bot))
    
def errorfuntion(Bot: commands.Bot):
    Bot.add_cog(errors(Bot))
    
#HelpCogHostType
if host == "dev":
    from modules.help import HelpCog
    def helpfuntion(bot: commands.Bot):
        bot.add_cog(HelpCog(bot))
    helpfuntion(Bot)
if host != "dev":
    if host == "replit":
        @Bot.command()
        async def help(ctx):
            await ctx.send("El comando: help. Esta desabilitado debido a un error. \n \n Puedes ver los comandos en: \n https://akazarbweb.k1ngdev-server.repl.co/commands")
    if host != "replit":
        print(f"{Fore.RED} ******************************************************************* {Style.RESET_ALL}")
        print(f"{Fore.RED} El Host No es un Host Oficial hacegurate de que este bien escrito {Style.RESET_ALL}")
        print(f"{Fore.RED} ******************************************************************* {Style.RESET_ALL}")
        @Bot.command()
        async def help(ctx):
            await ctx.send("El comando: help. Esta desabilitado debido a un error. \n \n Puedes ver los comandos en: \n https://akazarbweb.k1ngdev-server.repl.co/commands")
            
#RunBot

funfuntion(Bot)
Bot.loop.create_task(setup(Bot))
keep_alive.keep_alive()
Bot.run(token)