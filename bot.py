import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
import config

# Загрузка переменных окружения (токен)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Настройка интентов (прав)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # Нужно для добавления в треды и выдачи ролей

class DualServerBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!', 
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # Загрузка когов (расширений)
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f'[+] Загружен ког: {filename}')
        
        # Синхронизация слеш-команд с серверами
        # Мы синхронизируем только с указанными гильдиями для мгновенного обновления
        guild_main = discord.Object(id=config.GUILD_MAIN_ID)
        guild_red = discord.Object(id=config.GUILD_RED_ID)
        
        self.tree.copy_global_to(guild=guild_main)
        self.tree.copy_global_to(guild=guild_red)
        
        await self.tree.sync(guild=guild_main)
        await self.tree.sync(guild=guild_red)
        print("[+] Команды синхронизированы с серверами MAIN и RED")

    async def on_ready(self):
        print(f'[+] Бот запущен как {self.user} (ID: {self.user.id})')
        print(f'[+] Подключен к {len(self.guilds)} серверам')

bot = DualServerBot()

if __name__ == '__main__':
    if not TOKEN:
        print("ОШИБКА: Токен не найден в .env файле")
    else:
        bot.run(TOKEN)
