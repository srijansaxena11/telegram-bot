from telethon import TelegramClient, events, sync

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'

bot = TelegramClient(bot_token = os.environ["TG_BOT_TOKEN"], api_id = int(os.environ["APP_ID"]), api_hash = os.environ["API_HASH"])
bot = TelegramClient('MyBot', os.environ["APP_ID"], os.environ["API_HASH"]).start(bot_token=BOT_TOKEN)
bot.start()

print(bot.get_me().stringify())

# bot.send_message('username', 'Hello! Talking to you from Telethon')
# bot.send_file('username', '/home/myself/Pictures/holidays.jpg')

# bot.download_profile_photo('me')
# messages = bot.get_messages('username')
# messages[0].download_media()

@bot.on(events.NewMessage(pattern='(?i)hi|hello'))
async def handler(event):
    await event.respond('Hey!')