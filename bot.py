import datetime
import calendar
from dotenv import load_dotenv
import os
import discord
from discord.ext import tasks, commands
from discord.ext.commands import Bot

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
    start_date = datetime.datetime(now.year, now.month, 8)
    end_date = datetime.datetime(now.year, now.month, min(12, last_day_of_month))

    if start_date <= now <= end_date:
        for guild in client.guilds:
            for channel_name in ALLOWED_CHANNELS:
                channel = discord.utils.get(guild.channels, name=channel_name)

                if channel:
                    embed = discord.Embed(
                        title='Message from Gorpa-Masorpa',
                        description='',
                        color=0x808000
                    )
                    embed.add_field(name='Hey Adventures!', value='This is your daily reminder from me, Gorpa-Masorpa! Please spend your hallmarks before the next update, or you\'ll lose them! \n\n You can find the next update schedule on [PlayOnline]({})'.format(patchday_url), inline=False)
                    embed.set_footer(text=footer_text.format(year=now.year, url=github_url))
                    await channel.send(embed=embed)

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
