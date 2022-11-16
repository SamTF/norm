### IMPORTS        ############################################################
# My modules
import jokes
# Stdlib
import json
from random import randrange
import asyncio
# Discord
import discord
from discord.ext import commands, tasks
from discord import app_commands
# FFMPEG
from discord import FFmpegPCMAudio


###### CONSTANTS        ##########################################################
TOKEN_FILE = '.norm.token'
NORM_GIF = 'https://i.imgur.com/CKj8b6T.gif'
JOKES = None

def load_jokes() -> dict:
    with open('jokes.json', 'r') as f:
        jokes = json.load(f)
        print(f'[NORM.PY] >>> Loaded {len(jokes)} jokes!')

        return jokes


###### DISCORD STUFF ############################################################
### Creating the bot!
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='🤘', intents=intents)

    # on_ready event l think
    async def setup_hook(self) -> None:
        await self.tree.sync(guild=discord.Object(id=349267379991347200))
        print(f'Synced slash commands for {self.user} @ server 349267379991347200')
    
    # error handling
    async def on_command_error(self, ctx, error) -> None:
        await ctx.reply(error, ephemeral=True)

bot = Bot()


###### EVENTS        ##########################################################
# Runs this when the bot becomes online
@bot.event
async def on_ready():
    print("I didn't even know he was sick!")
    print(bot.user.name)
    await bot.change_presence(activity=discord.Game("It's time to do jokes"))


###### COMMANDS        #######################################################
### /jokes
@bot.hybrid_command(name = 'joke', description = 'Read a joke for the folks at home')
@app_commands.guilds(discord.Object(id=349267379991347200))
async def joke(ctx):
    i = randrange(0, len(JOKES))
    joke = JOKES[i]

    print(i)
    print(f"[NORM.PY] >>> {joke}")

    # sending joke as an embed
    embed = discord.Embed(
        title=f'{joke.episode} w/ {joke.guest}',
        description=joke.joke,
        colour=0x2596be
        # url=concert.url,
    )
    embed.set_thumbnail(url=joke.thumbnail)
    embed.set_image(url=NORM_GIF)

    await ctx.send(embed = embed)


### VOICE COMMANDS
@bot.hybrid_command(name = '911', description = 'For when you need a reminder of that tragedy ;)')
@app_commands.guilds(discord.Object(id=349267379991347200))
async def nine_eleven(ctx):
    print(f"[NORM.PY] >>> {ctx.author} requested a joke")

    # checking if the command author is in a voice channel
    if not ctx.author.voice:
        await ctx.send("You have to be in a voice channel to hear the joke. What are you, fucking retarded?", ephemeral = True)
        return
    
    # user feedback
    await ctx.send("It's time to do jokes! Everyone join the voice chat")

    # connecting to voice channel
    channel = ctx.author.voice.channel
    vc = await channel.connect()

    # playing the joke mp3 - and disconnecting from the voice channel after it ends
    source = FFmpegPCMAudio('audio/911_airlines.mp3')
    player = vc.play(
        source,
        after=lambda _: asyncio.run_coroutine_threadsafe(
            coro=vc.disconnect(),
            loop=vc.loop
        ).result()
    )


###### RUNNING THE BOT #################################################
if __name__ == "__main__":
    print("_____________NORM MACDONALD INITIALISED_____________")
    with open(TOKEN_FILE, 'r') as f:
        token = f.read()
    
    JOKES = jokes.get_jokes()
    print(f'[NORM.PY] >>> Loaded {len(JOKES)} jokes!')

    bot.run(token)