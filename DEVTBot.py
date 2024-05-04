#Welcome to shitty code!
import os
import discord
from discord.ext import commands
import json
import sys

#import asyncio
#TODO Asyncio пока не используется, в будующем он будет хранить токен.

#Путь к токену бота.
token_file_path = 'bot_token.json'

# Загрузка токена из JSON файла
with open(token_file_path, 'r') as f:
    token_data = json.load(f)
    TOKEN = token_data['token']

#Создание перем. с ботом.
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


#Основная инициализация бота
@bot.event
async def on_ready():
    print(f"{bot.user.name} теперь работает!")


#Проверяет, является ли автором сообщения бот
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

    print(f"{bot.user.name} получил сообщение : {message.content}, на сервере {message.guild}")
    # TODO должно писать инфу, но оно не пишет. Я не знаю почему.


#Команда 1
@bot.command()
async def get_avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar.url
    await ctx.send(f"{userAvatar}\n Вот твоя аватарка!")


bot.run(TOKEN)
