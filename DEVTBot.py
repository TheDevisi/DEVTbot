# // Welcome to shitty code! \\
import aiohttp
import discord
from discord.ext import commands
import json
import random
import asyncio
import nltk
from PIL import Image
import io 
import math
import datetime
import re
guild_with_disabled_filter = []


filter_settings_path = 'filter_settings.json'
token_file_path = 'bot_token.json'
weather_api_path = 'weather_api.json'
bad_words_path = 'bad_words.txt'
#Token path (for your bot). Put your token in bot_token.json or change path here.

# Downloading token from file
with open(token_file_path, 'r') as f:
    token_data = json.load(f)
    TOKEN = token_data['token']

#same as bot token, but for weather. put your token (for example OpenWeather) into weather_api.json. Or change path here.
with open(weather_api_path, 'r') as f:
    weather_data = json.load(f)
    weather_API_key = weather_data['api']

#loads swears from txt file
with open(bad_words_path, 'r') as f:
    bad_words = f.read().split('\n')

#loading filter settings from json file
def load_filter_settings():
    try:
        with open(filter_settings_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return "FILE NOT EXIST! PLEASE CREATE filter_settings.json"





#TODO Make this used in future

guild_settings = {}


#Bot init 
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
intents = discord.Intents.default()
intents.members = True

#Starting bot
@bot.event
async def on_ready():
    print(f"{bot.user.name} is now active!")


#Checking if message author a bot or not
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)


#Command to get profile picture.
@bot.slash_command(name='get_profile_picture', description='You will get your profile picture')
async def get_avatar(ctx, member: discord.Member = None):
    """Basicaly, just getting user's profile picture link and sends this into chat."""
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar.url
    await ctx.send(f"{userAvatar}\n Here is profile picture!")

#TODO Fix a "Activity not found. Start a new one?", remove link to pfp in message (for ex: https://cdn.discordapp.com/avatars/..)
#FIXME: I don't know how to fix it. Kill me

#Just some info about bot. Nothing interesting here. I should add here someting later.
@bot.slash_command(name='about', description='I will send you some info about me')
async def about(ctx):

    info = '''Thanks for interesting!
The first, then I've seen the light was in: 03.05.2024
My creator is Devisi
My first command which was helpful is "!get_avatar" (and you can't find in my source anymore)
I have GitHub repository with my code! https://github.com/TheDevisi/DEVTbot
And that's all for now!'''

    await ctx.send(info)

#Select number betwen min and max. Roll.
@bot.slash_command(name='roll', description='Rolls a random number between two given numbers.')
async def roll(ctx, min_num: int, max_num: int):
    """We using "random" to get random number in range.
        I think it understable here, i tryed to write good code ^_^"""
    if min_num >= max_num:
        await ctx.send("Invalid range! The minimum number must be less than the maximum number.")
        return
    
    random_number = random.randint(min_num, max_num)
    await ctx.send(f"The random number between {min_num} and {max_num} is: {random_number}")



#Swowing weather for a specified location (from user input. e.g Moscow) 
@bot.slash_command(name='weather', description='Shows the weather for a specified location.')
async def weather(ctx, location: str):
    """Here we using OpenWeather API Key for getting weather.
        If you want put your API key go to line 25 for instruction.
        IF YOU DON'T WANT THIS FEATURE (sadly :( ) just remove this function """
    api_key = weather_API_key
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    async with aiohttp.ClientSession() as session:
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }

        async with session.get(base_url, params=params) as resp:
            if resp.status != 200:
                await ctx.send(f"Failed to fetch weather data for {location}.")
                return

            data = await resp.json()

            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            city = data['name']

            await ctx.send(f"Weather in {city}: {weather_description}, Temperature: {temperature}°C, Humidity: {humidity}%")


#Just a simple coin flip game
@bot.slash_command(name='coin', description='Heads or Tails?')
async def roll(ctx):
    """The same as the roll, but we don't give choice to user."""
    choices = ["Heads", "Tails"]
    bot_choice = random.choice(choices)
    await ctx.send(f"The bot chose {bot_choice}!")

#/////////////////////////////////////////////////////////////////////////

#MODERATION COMMANDS (BAN, KICK, UNBAN, MUTE, UNMUTE)

#BAN a user
@bot.slash_command(name='ban',description='Bans a user.')

@commands.has_permissions(ban_members=True, administrator=True) #Checking permissions
async def ban(ctx, member: discord.Member, reason: str = None):
    if member.id == ctx.author.id: #If you want to BAN yourself and you want to get fucked  just remove these lines
        await ctx.respond("DUDE! YOU CAN'T BAN YOURSELF! :skull:") # ":skull" means skull emoji in discord (💀)
        return

    elif member.guild_permissions.administrator: #If user has adminstrator power he can't get banned
        await ctx.respond("You can't ban an administrator.")
        return

    if reason is None:
        reason = f"Not provided by {ctx.author}" #If user not provided reason to ban someone

    await member.ban(reason=reason)
    await ctx.respond(f"<@{ctx.author.id}> used ban to <@{member.id}> Reason: {reason}") #Output if user banned succesfully


#TODO MAKE THIS FUCKING WORK
#Kick a user
@bot.slash_command(name='kick', description='Kicks a user.')
async def kick(ctx, *, member):
    await ctx.guild.kick(member)
    await ctx.send(f"{member.mention} has been kicked.")
    return

#Mute a user
@bot.slash_command(name='mute', description='Mutes a user.')
async def mute(ctx, *, member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f"{member.mention} has been muted.")
    return

#Unmute a user
@bot.slash_command(name='unmute', description='Unmutes a user.')
async def unmute(ctx, *, member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} has been unmuted.")
    return

#Just clear chat
@bot.slash_command(name='clear', description='Clears the chat.')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit= int(amount))
    await ctx.send(f"{amount} messages have been cleared.")
    return

#Create a new role
@bot.slash_command(name='create_role', description='Creates a role.')
async def create_role(ctx, *, name):
    await ctx.guild.create_role(name=name)
    await ctx.send(f"Role {name} has been created.")
    return


#Deleting role
@bot.slash_command(name='delete_role', description='Deletes a role.')
async def delete_role(ctx, *, name):
    role = discord.utils.get(ctx.guild.roles, name=name)
    await role.delete()
    await ctx.send(f"Role {name} has been deleted.")
    return


@bot.slash_command(name='help', description='Shows all commands')
async def help(ctx):
    await ctx.send(f"Here is a list of all commands: \n!get_profile_picture \n!about \n!roll \n!weather \n!coin \n!ban \n!unban \n!kick \n!mute \n!unmute \n!clear \n!create_role \n!delete_role \n!help")
    return
@bot.slash_command(name='send_dm', description='Sends a message to a user')
async def send_dm(ctx, member: discord.Member, *, message):
    await member.send(message)
    await ctx.send(f"Message has been sent to {member.mention}.")
    return


    
@bot.slash_command(name='get_cat', description='Shows a random cat picture.')
async def  random_cat_from_google(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.thecatapi.com/v1/images/search') as resp:
            if resp.status!= 200:
                await ctx.send(f"Failed to fetch cat picture.")
                return

            data = await resp.json()

            cat_url = data[0]['url']

            await ctx.send(cat_url)

@bot.slash_command(name='get_dog', description='Shows a random dog picture.')
async def random_dog_from_google(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://dog.ceo/api/breeds/image/random') as resp:
            if resp.status!= 200:
                await ctx.send(f"Failed to fetch dog picture.")
                return

            data = await resp.json()

            dog_url = data['message']

            await ctx.send(dog_url)

@bot.slash_command(name='get_fox', description='Shows a random fox picture.')
async def random_fox_from_google(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://randomfox.ca/floof/') as resp:
            if resp.status!= 200:
                await ctx.send(f"Failed to fetch fox picture.")
                return

            data = await resp.json()

            fox_url = data['image']

            await ctx.send(fox_url)


@bot.slash_command(name='random_fact', description='Shows a random fact.')
async def get_random_fact(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://uselessfacts.jsph.pl/random.json?language=en') as resp:
            if resp.status!= 200:
                await ctx.send(f"Failed to fetch fact.")
                return

            data = await resp.json()

            fact = data['text']

            await ctx.send(fact)



@bot.slash_command(name='get_joke', description='Shows a random joke.')
async def get_random_joke(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://official-joke-api.appspot.com/random_joke') as resp:
            if resp.status!= 200:
                await ctx.send(f"Failed to fetch joke.")
                return

            data = await resp.json()

            joke = data['setup'] + "\n" + data['punchline']

            await ctx.send(joke)


@bot.slash_command(name='random_motivation', description='Generates random motivation.')
async def random_motivation(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.motivationalquotes.io/v1/motivation') as resp:
            if resp.status!= 200:
                await ctx.send(f"Failed to fetch motivation.")
                return

            data = await resp.json()

            motivation = data['content']

            await ctx.send(motivation)

        
#Detecting swears in user message and remove message. Swears loading from "bad_words" variable. More you can find at the start of the code.
#Also, make sure you have "bad_words.txt" file in the same directory as the bot. 
#And here i added command if administrator wants to delete the filter and allow swears again for specefic guild.
#If user want to enable filter again, he can use!enable_filter command.
#This shit loading guild id's from filter_settings.json which contains guild id's which have filter disabled. IF FILTER DISABLED, IT DOESENT WORK.  
#todo make this because now it doesent exist



bot.run(TOKEN)

