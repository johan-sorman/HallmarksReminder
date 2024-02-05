import datetime
import calendar
from dotenv import load_dotenv
import os
import discord
from discord.ext import tasks, commands
import sqlite3

load_dotenv()

#############################################################################
## Discord Configuration
#############################################################################

TOKEN = os.getenv('DISCORD_TOKEN_HALLMARKS')
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

patchday_url = 'http://www.playonline.com/ff11us/info/list_mnt.shtml'
github_url = 'https://github.com/johan-sorman?tab=repositories'
footer_text = '© {year} - Created by Melucine@Bahamut'.format(year=now.year)

#############################################################################
## Bot
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
    last_day_of_month = calendar.monthrange(now.year, now.month)[1]
    start_date = datetime.datetime(now.year, now.month, 1)
    end_date = datetime.datetime(now.year, now.month, min(7, last_day_of_month))

    if start_date <= now <= end_date:
        # Fetch the latest data from the database
        latest_update = get_latest_update()

        for guild in client.guilds:
            for channel_name in ALLOWED_CHANNELS:
                channel = discord.utils.get(guild.channels, name=channel_name)

                if channel:
                    if latest_update:
                        latest_update_date = latest_update[0]
                        print(f"Retrieved Date from DB: {latest_update_date}")

                        # Extract the year, month, and day from the retrieved date
                        latest_update_year, latest_update_month, _ = map(int, latest_update_date.split('-'))

                        # Print statements for debugging
                        print(f"now.month: {now.month}")
                        print(f"now.year: {now.year}")
                        print(f"latest_update_month: {latest_update_month}")
                        print(f"latest_update_year: {latest_update_year}")
                        print(f"Condition result: {latest_update_month == now.month and latest_update_year == now.year}")

                        # Check if the retrieved date is in the current month
                        if latest_update_month == now.month and latest_update_year == now.year:
                            embed = discord.Embed(
                                title='Message from Gorpa-Masorpa',
                                description='',
                                color=0x808000
                            )
                            embed.add_field(name='Hey Adventurers!', value='This is your daily reminder from me, Gorpa-Masorpa! Please spend your hallmarks before the next update, or you\'ll lose them!', inline=False)
                            embed.add_field(name='Next Version Update:', value=f'The next version update is expected to occur on **{latest_update_date}** \n\n You can find the next version update schedule on [PlayOnline]({patchday_url})', inline=False)                     
                            embed.set_footer(text=footer_text.format(year=now.year, url=github_url))
                            
                            print(f"Constructed Embed: {embed}")

                            await channel.send(embed=embed)
                        else:
                            embed = discord.Embed(
                            title='Message from Gorpa-Masorpa',
                            description='',
                            color=0x808000
                            )
                            embed.add_field(name='Hey Adventurers!', value='This is your daily reminder from me, Gorpa-Masorpa! Please spend your hallmarks before the next update, or you\'ll lose them!', inline=False)
                            embed.add_field(name='Next Version Update:', value=f'\n\n You can find the next version update on [PlayOnline]({patchday_url})',inline=False)                     
                            embed.set_footer(text=footer_text.format(year=now.year, url=github_url))
                            await channel.send(embed=embed)
                    else:
                            embed = discord.Embed(
                            title='Message from Gorpa-Masorpa',
                            description='',
                            color=0x808000
                            )
                            embed.add_field(name='Hey Adventurers!', value='This is your daily reminder from me, Gorpa-Masorpa! Please spend your hallmarks before the next update, or you\'ll lose them!', inline=False)
                            embed.add_field(name='Next Version Update:', value=f'\n\n You can find the next version update on [PlayOnline]({patchday_url})',inline=False)                     
                            embed.set_footer(text=footer_text.format(year=now.year, url=github_url))
                            await channel.send(embed=embed)


def get_latest_update():
    conn = sqlite3.connect('version_updates.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS VersionUpdates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_date TEXT,
            update_datetime DATETIME
        )
    ''')

    cursor.execute('''
        SELECT update_date
        FROM VersionUpdates
        ORDER BY id DESC
        LIMIT 1
    ''')

    latest_update = cursor.fetchone()

    conn.close()

    return latest_update


## !hm command
@client.command(name='hm')
async def send_message(ctx):
    if ctx.author.id == int(os.getenv('BOTADMIN')):
        if ctx.channel.name in ALLOWED_CHANNELS:
            embed = discord.Embed(
                title='Message from Gorpa-Masorpa',
                description='',
                color=0x808000
            )
            embed.add_field(name='Hey Adventures!', value='This is your daily reminder from me, Gorpa-Masorpa! Please spend your hallmarks before the next update, or you\'ll lose them! \n\n You can find the next update schedule on [PlayOnline]({})'.format(patchday_url), inline=False)
            embed.set_footer(text=footer_text.format(year=now.year, url=github_url))
            await ctx.send(embed=embed)
        else:
            allowed_channels_list = ', '.join(ALLOWED_CHANNELS)
            embed = discord.Embed(
                title='Error',
                description=f"Sorry! My master told me I'm only allowed to post in the following channels: {allowed_channels_list}",
                color=0xff0000
            )
            embed.set_footer(text=footer_text.format(year=now.year, url=github_url))
            await ctx.send(embed=embed)
    else:
        await ctx.send("You do not have permission to use this command.")

client.run(TOKEN)
