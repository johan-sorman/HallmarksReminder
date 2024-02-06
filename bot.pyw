import datetime
import calendar
import os
from dotenv import load_dotenv
import discord
from discord.ext import tasks, commands
import sqlite3

load_dotenv()

#############################################################################
## Discord Configuration
#############################################################################

TOKEN = os.getenv('DISCORD_TOKEN_HALLMARKS')
DB_PATH = os.getenv('DB_PATH')
ALLOWED_CHANNELS = ['bots', 'bot', 'bot-command', 'ambuscade']
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
client = commands.Bot(command_prefix='!', intents=intents)

#############################################################################
## Embed Configuration
#############################################################################
now = datetime.datetime.now()

version_update_url = 'http://www.playonline.com/ff11us/index.shtml'
reward_url = 'https://www.bg-wiki.com/ffxi/Category:Ambuscade#Rewards'
footer_text = '© {year} - Created by Melucine@Bahamut'.format(year=now.year)

#############################################################################
## Bot comes online
#############################################################################

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    daily_message.start()

#############################################################################
# Daily loop between 8th and 12th of the current month.
# The embedded message is the same for both the command and the looped message.
#############################################################################

@tasks.loop(hours=24)
async def daily_message():
    now = datetime.datetime.now()
    last_day_of_month = calendar.monthrange(now.year, now.month)[1]
    start_date = datetime.datetime(now.year, now.month, 1)
    end_date = datetime.datetime(now.year, now.month, min(12, last_day_of_month))

    if start_date <= now <= end_date:
        # Fetch the latest data from the database
        latest_update_date, latest_update_year = get_latest_update()

        for guild in client.guilds:
            for channel_name in ALLOWED_CHANNELS:
                channel = discord.utils.get(guild.channels, name=channel_name)

                if channel:
                    if latest_update_date and latest_update_year:
                        latest_update_month = latest_update_date.split(',')[1].strip().split()[0]
                        latest_update_month_num = list(calendar.month_name).index(latest_update_month)

                        if int(latest_update_month_num) == now.month and int(latest_update_year) == now.year:
                            embed = discord.Embed(
                                title='✉️  Message from Gorpa-Masorpa ✉️ ',
                                description='',
                                color=0x808000)
                            
                            embed.add_field(name='Hey Adventurers!', value=f'This is your daily reminder from me, Gorpa-Masorpa! Please spend your [Hallmarks]({reward_url}) and [Gallantry]({reward_url}) before the next update, or you\'ll lose them!\n\n ➡️ Come see me at (G-9) in Mhaura', inline=False)
                            embed.add_field(name='', value='', inline=False)
                            embed.add_field(name='Next Version Update:', value=f'The next version update is guesstimated to occur on \n\n `{latest_update_date}, {latest_update_year}`\n\n For accurate informaiton visit the Playonline website. \n You can find the next version update schedule [here]({version_update_url}).', inline=False)                     
                            embed.set_footer(text=footer_text)
                            await channel.send(embed=embed)

                        else:

                            embed = discord.Embed(
                            title='Message from Gorpa-Masorpa',
                            description='',
                            color=0x808000)

                            embed.add_field(name='Hey Adventurers!', value=f'This is your daily reminder from me, Gorpa-Masorpa! Please spend your [Hallmarks]({reward_url}) and [Gallantry]({reward_url}) before the next update, or you\'ll lose them!\n\n ➡️ Come see me at (G-9) in Mhaura', inline=False)
                            embed.add_field(name='', value='', inline=False)
                            embed.add_field(name='Next Version Update:', value=f'The next version update is guesstimated to occur on \n\n `None`\n\n For accurate informaiton visit the Playonline website. \n You can find the next version update schedule [here]({version_update_url}).', inline=False)                     
                            embed.set_footer(text=footer_text)
                            await channel.send(embed=embed)

                    else:
                            
                            embed = discord.Embed(
                            title='Message from Gorpa-Masorpa',
                            description='',
                            color=0x808000)

                            embed.add_field(name='Hey Adventurers!', value=f'This is your daily reminder from me, Gorpa-Masorpa! Please spend your [Hallmarks]({reward_url}) and [Gallantry]({reward_url}) before the next update, or you\'ll lose them!\n\n ➡️ Come see me at (G-9) in Mhaura', inline=False)
                            embed.add_field(name='', value='', inline=False)
                            embed.add_field(name='Next Version Update:', value=f'The next version update is guesstimated to occur on \n\n `None`\n\n For accurate informaiton visit the Playonline website. \n You can find the next version update schedule [here]({version_update_url}).', inline=False)                     
                            embed.set_footer(text=footer_text)
                            await channel.send(embed=embed)


def get_latest_update():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure the table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_date TEXT,
            update_datetime DATETIME,
            year TEXT
        )
    ''')

    # Select the latest update date and year
    cursor.execute('''
        SELECT update_date, year
        FROM updates
        ORDER BY id DESC
        LIMIT 1
    ''')

    # Fetch the result
    latest_update = cursor.fetchone()

    conn.close()

    # Return the latest update date and year
    return latest_update[0], latest_update[1] if latest_update else (None, None)
client.run(TOKEN)
