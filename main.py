from telethon import TelegramClient, events
import os

api_id = int(os.environ.get("34577885"))
api_hash = os.environ.get("a2ee479674d5b5311dd00298ee51a500")

source_channel = "Atach_toptan"
target_channel = "Stepxwomenpajamas"
markup = 1.3

client = TelegramClient("session", api_id, api_hash)

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'toptan|wholesale|atach', '', text, flags=re.I)

    def change_price(match):
        price = float(match.group(1))
        return f"${round(price*markup,2)}"

    text = re.sub(r'\$(\d+(\.\d+)?)', change_price, text)
    return text.strip()

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    caption = clean_text(event.text)

    if event.photo:
        await client.send_file(target_channel, event.photo, caption=caption)
    else:
        await client.send_message(target_channel, caption)

client.start()
print("RUNNING...")
client.run_until_disconnected()
