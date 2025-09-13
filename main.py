import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import datetime


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Define the time for the daily message (e.g., 10 AM UTC)
daily_announcement_time = datetime.time(hour=7, minute=46, tzinfo=datetime.timezone.utc)


@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}!")
    if not daily_message_task.is_running():
        daily_message_task.start()


@tasks.loop(time=daily_announcement_time)
async def daily_message_task():
    # Replace YOUR_CHANNEL_ID with the actual ID of the channel
    # where you want the message to be sent.
    channel_id = 1416325078420820141 
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("Good morning! Here's your daily update.")
    else:
        print(f"Channel with ID {channel_id} not found.")

@daily_message_task.before_loop
async def before_daily_message_task():
    # This function runs before the loop starts, allowing for setup or waiting.
    # In this case, it ensures the bot is ready before attempting to send messages.
    await bot.wait_until_ready()
    print("Daily message task is ready to start.")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)