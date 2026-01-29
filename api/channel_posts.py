from fastapi import FastAPI
from telethon import TelegramClient
from telethon.sessions import StringSession

app = FastAPI()

# ======================
# TELEGRAM CONFIG
# ======================
API_ID = 27634392
API_HASH = "c29325ca5de227dc611e54d355f76896"
SESSION_STRING = "1BVtsOL8Buzsgrn4bQR05-TpOpiA-Yuv_9PW59QlwCJ-I6f8rDG82wmH_u9QYUz1qRoJkdzwsrwxvdNVqUpnKCigOYuxMd3DOBVr9JpV2_o_C-icsZI3x13YX68BkICDHCJhti3fxdzwcTad9CjLaG9Nn0FhapUwwg_mqoThVQ9jaTk9sX6eLAbvah72KNP4rRk1k2HuE9uKULX-0wbi_YWnymYcAklh9QXSo9ID8HYnS6axzXa2ygn7lRqjGQqYYo_0kkeCWYc-4_p0rjt3OkiVrlUXGrsR7ivDRgeLDkjprC2PUlLTgkCaeqP6FFVK-UsNphG6ix-__ZD32gnAcXaEmlWxLJkM="
CHANNEL_ID = -1001169143349
# ======================


@app.get("/channel/posts")
async def get_last_posts(limit: int = 10):
    client = TelegramClient(
        StringSession(SESSION_STRING),
        API_ID,
        API_HASH
    )

    await client.connect()

    if not await client.is_user_authorized():
        await client.disconnect()
        return {
            "error": "Telegram session is not authorized"
        }

    messages = await client.get_messages(CHANNEL_ID, limit=limit)

    posts = []
    for msg in messages:
        posts.append({
            "message_id": msg.id,
            "date": msg.date.isoformat() if msg.date else None,
            "text": msg.text,
            "views": msg.views,
            "forwards": msg.forwards,
            "replies": msg.replies.replies if msg.replies else 0
        })

    await client.disconnect()

    return {
        "channel_id": CHANNEL_ID,
        "count": len(posts),
        "posts": posts
    }
