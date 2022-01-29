from ast import keyword
from distutils import command
from importlib.resources import path
from types import MemberDescriptorType
import discord
import requests
import json
import asyncio
import youtube_dl
import pafy
from discord.ext import commands
from discord.ext.commands import bot
from keep_alive import keep_alive
import asyncio
import os
from replit import db
import random

TOKEN="OTM2OTY2OTM1MDkzMDc1OTk4.YfU4dQ.1Bzgxkr7eTKE5mTok0i8B9GcWDE"

# we can use any symbol or charector as command prefix

client=commands.Bot(command_prefix="$")
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

sad_words={'sad','feeling down','wish somebody was here for me','depressed','depression','misearable','unhappy','angry'}

starter_encouragements = [
  'Cheer up!!!',
  'Hang in there.',
  'You are a great person.'
]

thank_words={'thank you','your help','i feel better', 'i feel good','your great help'}

starter_thanks = [
  'Always happy to help',
  'No problem at all'
]

bad_words={'fuck', 'you suck','suck','porn','sex'}

starter_bad = [
  'This message is inappropriate and goes against our community headlines'
]

movies = [
    "https://www.imdb.com/title/tt0084827/",
    "https://www.imdb.com/title/tt0113243/",
    "https://www.imdb.com/title/tt0168122/",
    "https://www.imdb.com/title/tt0218817/",
    "https://www.imdb.com/title/tt1285016/",
    "https://www.imdb.com/title/tt2234155/",
    "https://www.imdb.com/title/tt2357129/",
    "https://www.imdb.com/title/tt2084970/",
    "https://www.imdb.com/title/tt0470752/"
]

tv = [
  "https://www.imdb.com/title/tt2575988/",
  "https://www.imdb.com/title/tt4158110/",
  "https://www.imdb.com/title/tt7826376/",
  "https://www.imdb.com/title/tt2085059/",
  "https://www.imdb.com/title/tt0475784/",
  "https://www.imdb.com/title/tt3514324/",
  "https://www.imdb.com/title/tt1839578/",
  "https://www.imdb.com/title/tt0487831/",
  "https://www.imdb.com/title/tt0934814/",
  "https://www.imdb.com/title/tt2543312/",
  "https://www.imdb.com/title/tt14245530/",
  "https://www.imdb.com/title/tt13920422/"
]

animes = [
  "https://www.imdb.com/title/tt1587391/",
  "https://www.imdb.com/title/tt0113568/",
  "https://www.imdb.com/title/tt1474276/",
  "https://www.imdb.com/title/tt3613454/",
  "https://www.imdb.com/title/tt2859246/",
  "https://www.imdb.com/title/tt1587391/",
  "https://www.imdb.com/title/tt14675322/",
  "https://www.imdb.com/title/tt0500092/",
  "https://www.imdb.com/title/tt0328832/"
]

rules = [""":one: General Rules

1.1 - No overly long nicknames.
1.2 - No sexually explicit nicknames. 
1.3 - No offensive nicknames.
1.4 - No sexually explicit profile pictures.
1.5 - No offensive profile pictures.
1.6 - No membership granted to children (under 13 years of age).
1.7 - Moderators reserve the right to change nicknames.
1.8 - Moderators reserve the right to use their own descretion regardless of any rule.
1.9 - Respect the staff they are working for you.
1.10 - No exploiting loopholes in the rules (please report them).
1.11 - No bugs, exploits, glitches, hacks, spamming, etc.
1.12 - All server rules apply to DM's (advertising, server invites, nsfw, gore, etc.)
1.13 - Check the pins for newest informations about rules.
1.14 - raiding other communities/ harassment is an instant ban."""
,
""":two: Text Chat Rules

2.1 - No asking to be granted roles/moderator roles.
2.2 - @mention the moderators for support. 
2.3 - No spam of any type (Mentioning spam).
2.4 - No publishing of personal information (including adresses, emails, bank account, credit card information, etc.).
2.5 - No hate speech (mentioning killing, hurting, burning, etc. groups of individuals).
2.6 - No encouraging suicide or wishing death.
2.7 - No slurs. (n slur, f slur, r slur).
2.8 - No e-dating.
2.9 - Agree to disagree.
2.10 - No disrupting the peace of the chat.
2.11 - No walls of text (over 5 lines).
2.12 - No ascii (art in the form of text/dots).
2.13 - No overusing emojis and reactions.
2.14 - Moderators reserve the right to delete any post.
2.15 - No advertisement or links.
2.16 - Bot commands only under bot-commands.
2.17 - No off topic/use the right text channel for the topic you wish to discuss.
2.18 - No slur bypassing. (spoilers included)."""
,""":three: Voice Chat Rules

3.1 - No annoying, loud or high pitch noises.
3.2 - Reduce the amount of background noise, if possible.
3.3 - Moderators reserve the right to disconnect, mute, deafen or move members to and from voice channels.
3.4 - no gore/nsfw or disturbing activity allowed in streams, could result to instant ban"""
,""":four: Content Rules

4.1 - No NSFW.
4.3 - No earrape in content
4.4 - No content relating to cars crashing or people getting hit by cars.
4.5 - No epileptic content (gifs, vidoes, emotes).
4.6 - No offensive content (KKK, 9/11, George Floyd, Nazi, burning flags,  etc.)
4.7 - Rules relating to slurs apply to content posted."""
,""":five: Bot Rules

5.1 - Don't play NSFW music with Music bots. 
5.2 - Don't play Earrape with Music bots. 
5.3 - Dont play music that encourages racism or discrimination in public vcs 
5.4 - Music that heavily uses slurs or racial terms is inappropriate for server use. 
5.5 - Don't skip music constantly. 
5.6 - Country commands can't be used to commit Hate Speech! 
5.7 - Country commands can't be used to bypass the N word! 
5.8 - Using alts to gain more money in UnbelievaBoat games is prohibited."""
,""":six: Partnership rules Rules

6.1 - Must have at least 10,000 members in your server.
6.2 - Server can not be NSFW orientated. """]



@client.event
async def on_ready():
    if "json" in db.keys():
        del db['json']
    print("The Bot is ready")

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")

#ctx means context

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "-" + json_data[0]["a"]
  return(quote)


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

"""TO SHOW THE RULES"""
#aliases allows you to add similar words which gives the same functions as rule

@client.command(aliases=["rules","rule no","r"])
async def rule(ctx,*,number):
    await ctx.send(rules[int(number)-1])


"""TO DELETE THE MESSAGES"""
#amount = 1 +1 is a default (the command + previous message is deleted.)
@client.command(aliases=["c","delete","d"])
#for moderators to be seen the delted messages by bot use the below command
#@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=1):
    await ctx.channel.purge(limit = amount+1)




"""BOT REACTING WITH EMOJIS"""
"""1.bot reacting to Hello"""
@client.command(aliases=["Hello","hi","Hi","HI","HELLO"])
async def hello(ctx):
    await ctx.send(f"hello  {str(ctx.message.author)}  😄")


words=["awesome","thanks","thankyou","perfect","perfection","cool","kind","nice","love","best"]
critics=["bad","stupid","fool","not working","idiot"]
banned_words=["fuck","fucker","hentai","xnxx","nigga","horny","xhamster","xvideos"]

"""2.bot reacting to welcoming words"""
@client.event
async def on_message(message):
  #"""4.BOT DELETING BANNED WORDS"""
    for i in range(len(banned_words)):
        if banned_words[i] in message.content:
          await message.channel.purge(limit = 1)
          await message.channel.send(f"⚠️ This message is inappropriate and goes against the community guidelines. {message.author}")

    for i in range (len(words)):
        if words[i] in message.content:
            await message.channel.send("Aww Thank You 😚")

#"""3.bot reacting to criticizing words"""
    for i in range (len(critics)):         
        if critics[i] in message.content:
            await message.channel.send("I'm sorry 🥺, my developers are looking onto it...😔")

    if message.author == client.user:
      return

  
    options=starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))

    options=starter_thanks
    if "thanks" in db.keys():
      options = options + list(db["thanks"])

    if any(word in message.content for word in thank_words):
      await message.channel.send(random.choice(starter_thanks))

    options=starter_bad
    if "bad" in db.keys():
      options = options + list(db['bad'])
      
    if any(word in message.content for word in bad_words):
      await message.channel.send(random.choice(starter_bad))

    if message.content.startswith("$new"):
      encouraging_message = message.content.split("$new ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New encouraging message added.")

    if message.content.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(message.content.split("$del",1)[1])
        delete_encouragment(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if "thanks" in message.content:
      await message.channel.send("No problem, I am always happy to help you.")

    if message.content.startswith('*list'):
      encouragements=[]
      if "encouragements" in db.keys():
        encouragements=db["encouragements"]
      await message.channel.send(encouragements)

    if message.content.startswith("$responding"):
      value=message.contents.split("$responding ",1)[1]
      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off.")


    await client.process_commands(message)



############################################################     MAIN PART      ################################
"""~make me laugh : produces funny memes"""
@client.command(aliases=["memes","meme","funny"])
async def make(ctx):
    path=random.choice(os.listdir("tech_memes"))
    await ctx.send(file=discord.File(f"tech_memes/{str(path)}"))



"""~pics"""
@client.command(aliases=["picture","wallpaper","image","img","pics"])
async def pic(ctx):
    path=random.choice(os.listdir("tech_pics"))
    await ctx.send(file=discord.File(f"tech_pics/{str(path)}"))



"""~anime_pics"""
@client.command()
async def anime_pics(ctx):
    path=random.choice(os.listdir("anime_pics"))
    print(path)
    await ctx.send(file=discord.File(f"anime_pics/{str(path)}"))

@client.command()
async def inspire(ctx):
  quote=get_quote()
  await ctx.send(quote)


"""~anime_memes"""
@client.command()
async def anime_memes(ctx):
    path=random.choice(os.listdir("anime_memes"))
    print(path)
    await ctx.send(file=discord.File(f"anime_memes/{str(path)}"))

############################################################     MUSIC BOT     ################################


@client.command()
async def helpme(ctx):
  await ctx.send("\n$search: Search for questions on stackoverflow by just typing $search ``your question`` \n$movie: Get movie suggestions from our bot by just typing in $movie\n$shows: Get TV-series suggestions from our bot by just typing in $movie\n$anime: Get anime suggestions from our bot by just typing in $movie\n!join: Let the bot join your voice chat\n!play: Play a music by just typing in !play ``song name``\n!pause: Pause the music by just typing in !pause\n!resume: Resume the music by just typing in !resume\n!leave: Remove the bot from the voice room by just typing in !leave\n!queue: Displays the playlist\n!skip: Skip the music and move on to the next song in the playlist by typing in !skip\n$inspire: Sends motivational quotes\n$tech_pics: Sends technology stack images\n$tech_meme: Sends memes related to programming\n$anime_pics: Sends anime images on command\n$anime_memes: Sends anime memes on command\n$rule: Displays the rules by typing in $rule ``any number from 1-6``\n$d: It can delete the messages above by just typing in $d ``i`` where i is the number of messages you want to delete\n")


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(
            None, lambda: youtube_dl.YoutubeDL({
                "format": "bestaudio",
                "quiet": True
            }).extract_info(f"ytsearch{amount}:{song}",
                            download=False,
                            ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"]
                for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(url)),
                              after=lambda error: self.bot.loop.create_task(
                                  self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send(
                "You are not connected to a voice channel, please connect to the channel you want the bot to join."
            )

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("I am not connected to a voice channel.")

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("You must include a song to play.")

        if ctx.voice_client is None:
            return await ctx.send(
                "I must be in a voice channel to play a song.")

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for song, this may take a few seconds.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send(
                    "Sorry, I could not find the given song, try using my search command."
                )

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(
                    f"I am currently playing a song, this song has been added to the queue at position: {queue_len+1}."
                )

            else:
                return await ctx.send(
                    "Sorry, I can only queue up to 10 songs, please wait for the current song to finish."
                )

        await self.play_song(ctx, song)
        await ctx.send(f"Now playing: {song}")

    # @commands.command()
    # async def search(self, ctx, *, song=None):
    #     if song is None:
    #         return await ctx.send("You forgot to include a song to search for."
    #                               )

    #     await ctx.send("Searching for song, this may take a few seconds.")

    #     info = await self.search_song(5, song)

    #     embed = discord.Embed(
    #         title=f"Results for '{song}':",
    #         description=
    #         "*You can use these URL's to play an exact song if the one you want isn't the first result.*\n",
    #         colour=discord.Colour.red())

    #     amount = 0
    #     for entry in info["entries"]:
    #         embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
    #         amount += 1

    #     embed.set_footer(text=f"Displaying the first {amount} results.")
    #     await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx):  # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue.")

        embed = discord.Embed(title="Song Queue",
                              description="",
                              colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="Thanks for using me!")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any song.")

        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel."
                                  )

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send(
                "I am not currently playing any songs for you.")

        poll = discord.Embed(
            title=
            f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}",
            description=
            "**80% of the voice channel must vote to skip for it to pass.**",
            colour=discord.Colour.blue())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Voting ends in 15 seconds.")

        poll_msg = await ctx.send(
            embed=poll
        )  # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705")  # yes
        await poll_msg.add_reaction(u"\U0001F6AB")  # no

        await asyncio.sleep(15)  # 15 seconds to vote

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
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (
                    votes[u"\u2705"] +
                    votes[u"\U0001F6AB"]) > 0.79:  # 80% or higher
                skip = True
                embed = discord.Embed(
                    title="Skip Successful",
                    description=
                    "***Voting to skip the current song was succesful, skipping now.***",
                    colour=discord.Colour.green())

        if not skip:
            embed = discord.Embed(
                title="Skip Failed",
                description=
                "*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 80% of the members to skip.**",
                colour=discord.Colour.red())

        embed.set_footer(text="Voting has ended.")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("I am already paused.")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if not ctx.voice_client.is_paused():
            return await ctx.send("I am already playing a song.")

        ctx.voice_client.resume()
        await ctx.send("The current song has been resumed.")


async def setup():
  await bot.wait_until_ready()
  bot.add_cog(Player(bot))


bot.loop.create_task(setup())










############################################################     ABHINAV'S PART      ################################

@client.command()
async def search(ctx, *, query):
    if not query.isnumeric():
        response = requests.get(
            f"https://api.stackexchange.com/2.3/search?page=1&order=desc&sort=relevance&intitle={query}&site=stackoverflow&filter=!6VvPDzQywlcE5"
        )
        json_data = json.loads(response.text.replace("items", "abhis", 1))
        if len(json_data['abhis']) > 5:
            db["json"] = json_data
            author = ctx.author.mention
            await ctx.channel.send(
                f"Here are some few similar questions asked on stackoverflow {author} ! "
            )
            async with ctx.typing():
                for i in range(0, 5):
                    await ctx.send(
                        f"\n#{i+1} - {json_data['abhis'][i]['title']}")
            await ctx.send(
                f"\nWhich one of the questions matches the most? (type $search 1-5)"
            )
        else:
            await ctx.send("\nNot many links available.")
    else:
        if "json" in db.keys():
            if not db['json']['abhis'][int(query) - 1]['is_answered']:
                await ctx.send(
                    f"\nNobody answered this question {db['json']['abhis'][int(query)-1]['link']}"
                )
            elif 'accepted_answer_id' not in db['json']['abhis'][int(query) -
                                                                 1]:
                await ctx.send(
                    f"\nNo accepted answer so here is the link to browse all answers {db['json']['abhis'][int(query)-1]['link']}"
                )
                del db['json']
            else:
                await ctx.send(
                    f"\nHere is the accepted answer for that question {db['json']['abhis'][int(query)-1]['link']}/{db['json']['abhis'][int(query)-1]['accepted_answer_id']}/#{db['json']['abhis'][int(query)-1]['accepted_answer_id']}"
                )
                del db['json']
        else:
            await ctx.send("Please search for a question first")

@client.command()
async def movie(ctx):
  author = ctx.author.mention
  await ctx.channel.send(
      f"Here is a movie you might like! {author} ! "
  )
  async with ctx.typing():
    await ctx.send(movies[random.randint(0, len(movies))])

@client.command()
async def shows(ctx):
  author = ctx.author.mention
  await ctx.channel.send(
      f"Here is a TV series you might like! {author} ! "
  )
  async with ctx.typing():
    await ctx.send(tv[random.randint(0, len(tv))])

@client.command()
async def anime(ctx):
  author = ctx.author.mention
  await ctx.channel.send(
      f"Here is a anime you might like! {author} ! "
  )
  async with ctx.typing():
    await ctx.send(animes[random.randint(0, len(animes))])


"""ERROR HANDLING
try:
    command
except:
    command

    OR                           """
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send(f"please check your command again ")
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(f"please enter all the requirements")
        await ctx.message.delete()
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds.")
    else: 
        await ctx.send(f"Oh no! Something went wrong while running the command! 😥")



        

        
            
 
#to run the bot

keep_alive()
# bot.run(TOKEN)
# client.run(TOKEN)

loop = asyncio.get_event_loop()
loop.create_task(client.start(TOKEN))
loop.create_task(bot.start(TOKEN))
loop.run_forever()