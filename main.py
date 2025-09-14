import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import datetime
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start_server():
    HTTPServer(("0.0.0.0", int(os.getenv("PORT", 8000))), HealthHandler).serve_forever()

threading.Thread(target=start_server, daemon=True).start()


load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

list_comm_mod = [
    "PB Tutoring: How has your understanding of the challenges of human experience been shaped by your study of the prescribed text",
    "PB Tutoring:Through the sharing of stories, we become more aware of ourselves and our shared human experiences. Explore this statement with close reference to your prescribed text.",
    """PB Tutoring: Human experience resembles the battered moon that tracks us in cycles of light and darkness, of life and death, now seeking out and now stealing away from the sun that gives it light and symbolises eternity" - Eugene Kennedy
Using the above quote as a stimulus, discuss the ideas of the human experience explored in your prescribed text.""",
    """Ascham 2019
“The work of the author is not just to present an idea, to create characters, or tell a story. The author must present us as we truly are.”
To what extent is this statement true for your prescribed text?
""",
]
list_mod_a = [
    """Premier Tutors: The things that are said in literature are always the same. What is important is the way they are said.' – Jorge Luis Borges
Analyse the way in which key values can be reimagined within textual conversations. In your response, make close reference to the quotation and the pair of prescribed texts that you have studied in Module A.""",
    """Barker 2019
In exploring the dissonances between two texts, their different values are foregrounded.
Discuss this statement with close reference to your prescribed texts.
""",
    """Killara 2019
By examining the resonances and dissonances between a pair of texts, responders are able to come to a better understanding and appreciation of both texts. 
Discuss with reference to the prescribed texts set for study
""",
]
list_mod_b = [
    """PB Tutoring:
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
""",
    """
Hurlstone 2021
Texts which live on, live in our imaginations. John Mullan

To what extent does Eliot’s poetry continue to be appreciated through its ability to capture audience imaginations?

In your response, make close reference to the following extract and at least TWO poems set for study. 

I grow old ... I grow old ...
I shall wear the bottoms of my trousers rolled.
Shall I part my hair behind?   
Do I dare to eat a peach?
I shall wear white flannel trousers and walk upon the beach.
I have heard the mermaids singing, each to each.
I do not think that they will sing to me.
I have seen them riding seaward on the waves
Combing the white hair of the waves blown back
When the wind blows the water white and black.
We have lingered in the chambers of the sea
By sea-girls wreathed with seaweed red and brown
Till human voices wake us, and we drown.
""",
    """
Riverview 2019
Despite appearing fragmented and unstructured, Eliot’s poetry is both controlled and purposeful.

To what extent is this true? 

In your response make detailed reference to “Preludes” and at least ONE other poem set for study.
""",
]
list_mod_c = [
    """Art of Smart: 
(20 marks)
“No one should be ashamed to admit they are wrong, which is but saying, in other words, that they are wiser today than they were yesterday.” – Alexander Pope
Use this quote as a stimulus for a piece of persuasive, discursive or imaginative writing that expresses your perspective about a significant concern or idea that you have engaged with in ONE of your prescribed texts from Module A, B or C.
""",
    """
Art of Smart:
“The place comes first. If the place isn’t interesting to me then I can’t feel it. I can’t feel any people in it. I can’t feel what the people are on about or likely to get up to..” – Tim Winton

(a) Use this sentence as a stimulus for an imaginative, discursive or persuasive piece of writing which centres a strong connection between characters and place. In your response, you must include at least ONE literary device or stylistic feature that you have explored during your study of a prescribed text in Module C. (12 marks)

(b) Explain how at least ONE of your prescribed texts from Module C has influenced your writing style in part (a). In your response, focus on ONE literary device or stylistic feature that you have used in part (a). (8 marks)

""",
    """Art of Smart
“I am no bird; and no net ensnares me: I am a free human being with an independent will.”  – Charlotte Bronte

(a) Use this quote as a stimulus for a piece of persuasive, discursive or imaginative writing that expresses your perspective about a significant concern or idea that you have engaged with in ONE of your prescribed texts from Module A, B or C. (10 marks)

(b) Justify the creative decisions that you have made in your writing in part (a) by referencing your prescribed text. (10 marks)
""",
]
# Define the time for the daily message (e.g., 10 AM UTC)
daily_announcement_time = [
    datetime.time(hour=12, minute=55, tzinfo=datetime.timezone.utc)
]

global count
count = 0


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
        await channel.send(
            f"""Daily English Advanced Question Update

Common Module: 

{list_comm_mod[count]}

Mod A: 

{list_mod_a[count]}

Mod B: 

{list_mod_b[count]}

Mod C: 

{list_mod_c[count]}

"""
        )
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
