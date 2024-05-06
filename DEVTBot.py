# // Welcome to shitty code! \\
import aiohttp
import discord
from discord.ext import commands
import json
import random
import asyncio
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image
import io 
import math
import datetime

#Token's path and. If you downloaded this (why???) you should create bot.token.json in folder with this script. Or change path to bot token.
token_file_path = 'bot_token.json'
weather_api_path = 'weather_api.json'
# Downloading token from file
with open(token_file_path, 'r') as f:
    token_data = json.load(f)
    TOKEN = token_data['token']
# Same as token, but for weather api. If you want to use your own weather api, you should create weather_api.json in folder with this script. Or change path to weather api key.
with open(weather_api_path, 'r') as f:
    weather_data = json.load(f)
    weather_API_key = weather_data['api']


#Bot initialization
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


#Main bot initialization. Starting bot
@bot.event
async def on_ready():
    print(f"{bot.user.name} is now active!")


#Is message author a bot?
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)


#Getting user's profile picture
@bot.slash_command(name='get_profile_picture', description='You will get your profile picture')
async def get_avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar.url
    await ctx.send(f"{userAvatar}\n Here is profile picture!")

#TODO Fix a "Activity not found. Start a new one?", remove link to pfp in message (for ex: https://cdn.discordapp.com/avatars/..)


#Just some info about bot. Nothing interesting here. I should add here someting later.
@bot.slash_command(name='about', description='I will send you some info about me')
async def about(ctx):

    info = '''Thanks for interesting!
The first, then I've seen the light was in: 03.05.2024
My creator is Devisi
My first command which was helpful is "!get_avatar" (which you can't find in my source anymore)
I have GitHub repository with my code! https://github.com/TheDevisi/DEVTbot
And that's all for now!'''

    await ctx.send(info)

#Select number betwen min and max. Roll.
@bot.slash_command(name='roll', description='Rolls a random number between two given numbers.')
async def roll(ctx, min_num: int, max_num: int):
    if min_num >= max_num:
        await ctx.send("Invalid range! The minimum number must be less than the maximum number.")
        return
    
    random_number = random.randint(min_num, max_num)
    await ctx.send(f"The random number between {min_num} and {max_num} is: {random_number}")



#Swowing weather for a specified location (from user input. e.g Moscow) 
@bot.slash_command(name='weather', description='Shows the weather for a specified location.')
async def weather(ctx, location: str):
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
    choices = ["Heads", "Tails"]
    bot_choice = random.choice(choices)
    await ctx.send(f"The bot chose {bot_choice}!")

#/////////////////////////////////////////////////////////////////////////

#MODERATION COMMANDS (BAN, KICK, UNBAN, MUTE, UNMUTE)

#BAN a user
@bot.slash_command(name='ban', description='Bans a user.')
async def ban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned.")
            return

    await ctx.guild.ban(member)
    await ctx.send(f"{member.mention} has been banned.")

#UNBAN a user
@bot.slash_command(name='unban', description='Unbans a user.')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned.")
            return

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

#Random motivation quotes from file. Now doesent using, because I don't have motivation quotes for now
#TODO find motivation quotes and copy them to file 
#@bot.command(name='random_motivation', description='Generates random motivation')
#async def random_motivation(ctx):
    #with open('motivations.txt', 'r') as f:
        #motivations = f.read().splitlines()
        #random_motivation = random.choice(motivations)
        #await ctx.send(random_motivation)
        #return
    

@bot.slash_command(name='help', description='Shows all commands')
async def help(ctx):
    await ctx.send(f"Here is a list of all commands: \n!get_profile_picture \n!about \n!roll \n!weather \n!coin \n!ban \n!unban \n!kick \n!mute \n!unmute \n!clear \n!create_role \n!delete_role \n!help")
    return
@bot.slash_command(name='send_dm', description='Sends a message to a user')
async def send_dm(ctx, member: discord.Member, *, message):
    await member.send(message)
    await ctx.send(f"Message has been sent to {member.mention}.")
    return

#Detecting swearing from all users messagges removing them and warning a user
#Doesent work properly

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    if message.content.lower() == "fuck":
        await message.delete()
        await message.channel.send(f"{message.author.mention} You are not allowed to say that!")
        return
    if message.content.lower() == "shit":
        await message.delete()
        await message.channel.send(f"{message.author.mention} You are not allowed to say that!")
        return
    if message.content.lower() == "bitch":
        await message.delete()
        await message.channel.send(f"{message.author.mention} You are not allowed to say that!")
        return
    if message.content.lower() == "asshole":
        await message.delete()
        await message.channel.send(f"{message.author.mention} You are not allowed to say that!")
        return
    if message.content.lower() == "fucking":
        await message.delete()
        await message.channel.send(f"{message.author.mention} You are not allowed to say that!")
        return
    if message.content.lower() == "fucked":
        await message.delete()
        await message.channel.send(f"{message.author.mention} You are not allowed to say that!")
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

@bot.slash_command(name='actualtime', description='Shows the actual time in your timezone.')
async def get_actual_time(ctx):
    await ctx.send(datetime.datetime.now(datetime.timezone.utc).astimezone())
    return datetime.dat



# Dictionary to hold guild-specific settings
guild_settings = {}

@bot.slash_command(name='configure_greeting', description='Configures the greeting message and channel.')
@commands.has_permissions(administrator=True)
async def configure_greeting(ctx, channel: discord.TextChannel, *, message: str):
    # Store the configuration in the guild_settings dictionary
    guild_id = ctx.guild.id
    if guild_id not in guild_settings:
        guild_settings[guild_id] = {}
    guild_settings[guild_id]['greeting_channel'] = channel.id
    guild_settings[guild_id]['greeting_message'] = message
    await ctx.send(f"Greeting message and channel configured! Message: \"{message}\" will be sent in {channel.mention}")

#TODO Make this shit pinging user even with custom welcome message 
@bot.event
async def on_member_join(member):
    guild_id = member.guild.id
    if guild_id in guild_settings:
        settings = guild_settings[guild_id]
        if 'greeting_channel' in settings and 'greeting_message' in settings:
            channel = bot.get_channel(settings['greeting_channel'])
            if channel:
                # Send the greeting message in the specified channel
                greeting_message = settings['greeting_message'].replace("{user}", member.mention)  # Пинг пользователя
                await channel.send(greeting_message)
                # Send a DM to the new member
                try:
                    dm_message = settings['greeting_message'].replace("{user}", f"@{member.name}")  # Пинг пользователя в DM
                    await member.send(dm_message)
                except discord.Forbidden:
                    print(f"Couldn't send DM to {member.name}")


                               
bot.run(TOKEN)