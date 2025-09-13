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

list_comm_mod = ["PB Tutoring: How has your understanding of the challenges of human experience been shaped by your study of the prescribed text",
"PB Tutoring:Through the sharing of stories, we become more aware of ourselves and our shared human experiences. Explore this statement with close reference to your prescribed text.",
"""PB Tutoring: Human experience resembles the battered moon that tracks us in cycles of light and darkness, of life and death, now seeking out and now stealing away from the sun that gives it light and symbolises eternity" - Eugene Kennedy
Using the above quote as a stimulus, discuss the ideas of the human experience explored in your prescribed text."""]
list_mod_a = ["""Premier Tutors: The things that are said in literature are always the same. What is important is the way they are said.' – Jorge Luis Borges
Analyse the way in which key values can be reimagined within textual conversations. In your response, make close reference to the quotation and the pair of prescribed texts that you have studied in Module A."""]
list_mod_b = ["""PB Tutoring:
“You tossed a blanket from the bed,
You lay upon your back, and waited;
You dozed, and watched the night revealing
The thousand sordid images
Of which your soul was constituted;
They flickered against the ceiling.
And when all the world came back
And the light crept up between the shutters
And you heard the sparrows in the gutters,
You had such a vision of the street
As the street hardly understands;
Sitting along the bed’s edge, where
You curled the papers from your hair,
Or clasped the yellow soles of feet
In the palms of both soiled hands.”

In your view, how does Eliot’s portrayal of the complex nature of personal experience contribute to the enduring value of his poetry?
In your response, make detailed reference to Preludes and at least ONE other poem set for study.
"""]
list_mod_c = ["""Art of Smart: “No one should be ashamed to admit they are wrong, which is but saying, in other words, that they are wiser today than they were yesterday.” – Alexander Pope
Use this quote as a stimulus for a piece of persuasive, discursive or imaginative writing that expresses your perspective about a significant concern or idea that you have engaged with in ONE of your prescribed texts from Module A, B or C.
"""]
# Define the time for the daily message (e.g., 10 AM UTC)
daily_announcement_time = datetime.time(hour=8, minute=11, tzinfo=datetime.timezone.utc)


@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}!")
    if not daily_message_task.is_running():
        daily_message_task.start()


@tasks.loop(time=daily_announcement_time)
async def daily_message_task():
    # Replace YOUR_CHANNEL_ID with the actual ID of the channel
    # where you want the message to be sent.
    count = 0
    channel_id = 1416325078420820141 
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(f"""Daily English Advanced Question Update

Common Module: 

{list_comm_mod[count]}

Mod A: 

{list_mod_a[count]}

Mod B: 

{list_mod_b[count]}

Mod C: 

{list_mod_c[count]}

""")
        count += 1
    else:
        print(f"Channel with ID {channel_id} not found.")

@daily_message_task.before_loop
async def before_daily_message_task():
    # This function runs before the loop starts, allowing for setup or waiting.
    # In this case, it ensures the bot is ready before attempting to send messages.
    await bot.wait_until_ready()
    print("Daily message task is ready to start.")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)