import os
import discord
from discord.ext import commands
import json
import sys
import pycord

#import asyncio
#TODO Asyncio doesen't using, i'll rewrite code with it in the future to make it more safe

#Token's path. If you downloaded this (why???) you should create bot.token.json in folder with this script. Or change path to bot token.
token_file_path = 'bot_token.json'

# Downloading token from file
with open(token_file_path, 'r') as f:
    token_data = json.load(f)
    TOKEN = token_data['token']

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


bot.run(TOKEN)
