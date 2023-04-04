import os
import discord
from discord.ext import tasks, commands
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COIN_ID = os.getenv('COIN_ID')
API_URL = f'https://api.coingecko.com/api/v3/simple/price?ids={COIN_ID}&vs_currencies=usd'

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await update_bot_status()

async def fetch_price():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error fetching price for {COIN_ID}")
                return None

async def update_bot_status():
    while True:
        data = await fetch_price()
        if data and COIN_ID in data:
            price = data[COIN_ID]['usd']
            status = f"{COIN_ID.capitalize()} ${price}"
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        await asyncio.sleep(120)  # Update interval (in seconds)

bot.run(TOKEN)

