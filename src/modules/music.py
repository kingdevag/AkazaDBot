import asyncio
import youtube_dl
import pafy
import nextcord
from nextcord.ext import commands
from colorama import Fore
from colorama import Style

class Player(commands.Cog, name="Musica"):
    """Reproduce Musica"""
    COG_EMOJI = "🎧"
    
    def __init__(self, Bot):
        self.Bot = Bot 
        self.song_queue = {}
    
        self.setup()

    def setup(self):
        for guild in self.Bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.Bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(url)), after=lambda error: self.Bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Fore.RED} *+*+*--- Music.Cog Loaded Successfully ---*+*+* {Style.RESET_ALL}")
        
    @commands.command()
    async def join(self, ctx):
        """Mete al Bot en tu canal de Voz"""
        if ctx.author.voice is None:
            return await ctx.send("No está conectado a un canal de voz, conéctese al canal al que desea que se una el bot.")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        """Saca al Bot de Su canal de Voz"""
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("No estoy conectado a un canal de voz.")

    @commands.command()
    async def play(self, ctx, *, song=None):
        """Reproduce una cancion Mencionada"""
        if song is None:
            return await ctx.send("Debes incluir una canción para reproducir.")

        if ctx.voice_client is None:
            return await ctx.send("Debo estar en un canal de voz para reproducir una canción.")

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Buscando una canción, esto puede tardar unos segundos.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Lo siento, no pude encontrar la canción dada, intente usar search.")

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"Actualmente estoy reproduciendo una canción, esta canción se agregó a la cola en la posición: {queue_len+1}.")

            else:
                return await ctx.send("Lo siento, solo puedo poner en cola hasta 10 canciones, espere a que termine la canción actual.")

        await self.play_song(ctx, song)
        await ctx.send(f"Reproduciendo: {song}")

    @commands.command()
    async def search(self, ctx, *, song=None):
        """Busca una cancion"""
        if song is None: return await ctx.send("Olvidaste incluir una canción para buscar.")

        await ctx.send("Buscando una canción, esto puede tardar unos segundos.")

        info = await self.search_song(5, song)

        embed = nextcord.Embed(title=f"resultados para '{song}':", description="*Puede usar estas URL para reproducir una canción exacta si la que desea no es el primer resultado.*\n", colour=nextcord.Colour.red())
        
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Mostrando los primeros resultados de {amount}")
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx): # display the current guilds queue
        """Verifica las canciones que estan en Cola"""
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("Actualmente no hay canciones en la cola.")

        embed = nextcord.Embed(title="Song Queue", description="", colour=nextcord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="¡Gracias por usarme!")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        """Genera una Votacion para omitir la Cancion"""
        if ctx.voice_client is None:
            return await ctx.send("No estoy tocando ninguna canción.")

        if ctx.author.voice is None:
            return await ctx.send("No estás conectad@ a ningún canal de voz.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("Actualmente no estoy reproduciendo ninguna canción para ti.")

        poll = nextcord.Embed(title=f"Vota para saltar la canción de - {ctx.author.name}#{ctx.author.discriminator}", description="**80% of el canal de voz debe votar para saltar para que pase.**", colour=nextcord.Colour.blue())
        poll.add_field(name="Saltar", value=":white_check_mark:")
        poll.add_field(name="Quedarse", value=":no_entry_sign:")
        poll.set_footer(text="La votación termina en 15 segundos.")

        poll_msg = await ctx.send(embed=poll) # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705") # yes
        await poll_msg.add_reaction(u"\U0001F6AB") # no
        
        await asyncio.sleep(15) # 15 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)
        
        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79: # 80% or higher
                skip = True
                embed = nextcord.Embed(title="Saltada exitosamente", description="***La votación para omitir la canción actual fue exitosa, omitiéndola ahora.***", colour=nextcord.Colour.green())

        if not skip:
            embed = nextcord.Embed(title="Salto fallido", description="*La votación para omitir la canción actual ha fallado.*\n\n**La votación falló, la votación requiere que al menos el 80% de los miembros se salte.**", colour=nextcord.Colour.red())

        embed.set_footer(text="La votación ha terminado.")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()


    @commands.command()
    async def pause(self, ctx):
        """Pausa la Cancion"""
        if ctx.voice_client.is_paused():
            return await ctx.send("Ya estoy en pausa.")

        ctx.voice_client.pause()
        await ctx.send("La canción actual ha sido pausada.")

    @commands.command()
    async def resume(self, ctx):
        """Reanuda la reproduccion de una Cancion Pausada"""
        if ctx.voice_client is None:
            return await ctx.send("No estoy conectado a un canal de voz.")

        if not ctx.voice_client.is_paused():
            return await ctx.send("Ya estoy tocando una canción.")
        
        ctx.voice_client.resume()
        await ctx.send("La canción actual se ha reanudado..")

