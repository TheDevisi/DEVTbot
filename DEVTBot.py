import aiohttp
import discord
from discord.ext import commands
import json
import pycord
import random
import asyncio


#TODO Asyncio doesen't using, i'll rewrite code with it in the future to make it more safe

#Token's path. If you downloaded this (why???) you should create bot.token.json in folder with this script. Or change path to bot token.
token_file_path = 'bot_token.json'
weather_api_path = 'weather_api.json'
# Downloading token from file
with open(token_file_path, 'r') as f:
    token_data = json.load(f)
    TOKEN = token_data['token']

with open(weather_api_path, 'r') as f:
    weather_data = json.load(f)
    weather_API_key = weather_data['api']


#Bot init
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


#Main init
@bot.event
async def on_ready():
    print(f"{bot.user.name} is now active!")


#Checks if message author is not a bot
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)





#Get user's PFP
@bot.slash_command(name='get_profile_picture', description='You will get your profile picture')
async def get_avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar.url
    await ctx.send(f"{userAvatar}\n Here is profile picture!")

#TODO Fix a "Activity not found. Start a new one?", remove link to pfp in message (for ex: https://cdn.discordapp.com/avatars/..)

#Just sends some information about this bot
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



#Show's weather for user (yeah, i know, discord users doesen't know what is grass)
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

#Thats all for this day. I tired.
bot.run(TOKEN)
