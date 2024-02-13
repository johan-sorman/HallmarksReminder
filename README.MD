## Hallmarks Reminder

### What is this?
- A Simple bot to remind the users to spend their Hallmarks and Gallantry before next version update.
- It will work in two steps:
  1. `main.pyw` will scrape the Playonline website and assume the next version update date if SE has posted a version update announcement.
  2. After scraping the information and populating a local `.db` it will then use this information in the `bot.pyw`. 

### Cool, how does it work?
- Once per month the `main.pyw` will run to populate the `.db` file
- Between the 8th and 12th of the month, the bot will remind the users. If the date hasn't been fetched yet for the current month, it will still post a reminder but the next version update can be found on the Playonline website.

### Setup
The bot assumes at least one of the following channels:
`bot, bots, bot-command, ambuscade`
- Note that if you have multiple of these setups on your server for whatever reason, it will post in all of them. Therefore recommended to use one of those or restrict the bot from posting in the channel.
- Create env var values to `DB_PATH` and `Discord Token` (generated in Discord Developer Panel).

### Commands?
There are no commands, the bot works automatically. 
