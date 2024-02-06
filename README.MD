## Hallmarks Reminder

### What is this?
- A Simple bot to remind the users to spend their Hallmarks and Gallantry before next version update.
- It will work in two steps:
  1. `main.pyw` will scrape Playonline website and assume next version update date based on the `Login Points campaign`.
  2. After scraped the information and populated a local `.db` it will then use this information in the `bot.pyw`. 

### Cool, how does it actually work?
- Once per month the `main.pyw` will run to populate the `.db` file
- Between the 8th and 12th of the month, the bot will remind the users. If the date haven't been fetched yet for current month, it will still post a reminder but direct the next version update can be found on Playonline website.

### Setup
The bot assumes at least one of the follow channels:
`bot, bots, bot-command, ambuscade`
- Note that should you have multiple of these setup on your server for whatever reason, it will post in all of them. Therefor recommended just use one of those or restrict the bot to post in the channel.

### Commands?
There is no commands, the bot works automatically. 