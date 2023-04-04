import os
import discord
from discord.ext import tasks, commands
import requests
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COIN_ID = os.getenv('COIN_ID')  # Change this to the coin ID you want to track
API_URL = f'https://api.coingecko.com/api/v3/simple/price?ids={COIN_ID}&vs_currencies=usd'

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await update_bot_status()

async def update_bot_status():
    while True:
        response = requests.get(API_URL)
        data = response.json()
        if COIN_ID in data:
            price = data[COIN_ID]['usd']
            status = f"{COIN_ID.capitalize()} ${price}"
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        else:
            print(f"Error fetching price for {COIN_ID}")
        await asyncio.sleep(60)  # Update interval (in seconds)

bot.run(TOKEN)
