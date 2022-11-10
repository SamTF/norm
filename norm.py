### IMPORTS        ############################################################
# My modules
from thumb_scraper import get_thumb
# Stdlib
import json
from random import randrange
# Discord
import discord
from discord.ext import commands, tasks
from discord import app_commands


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
@bot.hybrid_command(name = 'jokes', description = 'Read a joke for the folks at home')
@app_commands.guilds(discord.Object(id=349267379991347200))
async def jokes(ctx):
    i = randrange(0, len(JOKES))
    joke = JOKES[i]

    print(f"[NORM.PY] >>> {joke['Joke']}")

    # sending joke as an embed
    embed = discord.Embed(
        title=joke['Episode'],
        description=joke['Joke'],
        colour=0x2596be
        # url=concert.url,
    )
    embed.set_thumbnail(url=get_thumb(joke['Guest']))
    embed.set_image(url=NORM_GIF)

    await ctx.send(embed = embed)


###### RUNNING THE BOT #################################################
if __name__ == "__main__":
    print("_____________NORM MACDONALD INITIALISED_____________")
    with open(TOKEN_FILE, 'r') as f:
        token = f.read()
    
    JOKES = load_jokes()

    bot.run(token)