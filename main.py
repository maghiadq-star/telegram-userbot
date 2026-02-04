from telethon import TelegramClient, events
import re, os

api_id = int(os.environ["34577885"])
api_hash = os.environ["a2ee479674d5b5311dd00298ee51a500"]

source_channel = 'Atach_toptan'
target_channel = 'Stepxwomenpajamas'

markup = 1.3

client = TelegramClient('session', api_id, api_hash)

def clean_text(text):
    if not text:
        return ''
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\+?\d[\d\s\-]{7,}', '', text)
    text = re.sub(r'toptan|wholesale|supplier|atach', '', text, flags=re.IGNORECASE)
    return text.strip()

def update_price(text):
    text = clean_text(text)
    def change(match):
        number = float(match.group(1))
        currency = match.group(3) or ''
        new_price = round(number * markup, 2)
        return f"{new_price} {currency}".strip()
    return re.sub(r'(\d+(\.\d+)?)\s?(TL|\$|€|USD)?', change, text)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    caption = update_price(event.text)

    if event.photo:
        await client.send_file(target_channel, event.photo, caption=caption)
    elif event.video:
        await client.send_file(target_channel, event.video, caption=caption)
    else:
        await client.send_message(target_channel, caption)

print("Bot running...")
client.start()
client.run_until_disconnected()
