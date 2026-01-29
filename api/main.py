from fastapi import FastAPI, HTTPException, Query
from telethon import TelegramClient
from telethon.sessions import StringSession

app = FastAPI()

# ======================
# TELEGRAM CONFIG
# ======================
API_ID = 27634392
API_HASH = "YOUR_API_HASH"
SESSION_STRING = "YOUR_SESSION_STRING"
CHANNEL_ID = -1001169143349
# ======================


@app.get("/channel/posts")
async def get_last_posts(limit: int = Query(10, ge=1, le=100)):
    client = TelegramClient(
        StringSession(SESSION_STRING),
        API_ID,
        API_HASH
    )

    await client.connect()

    try:
        if not await client.is_user_authorized():
            raise HTTPException(
                status_code=401,
                detail="Telegram session is not authorized"
            )

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

        return {
            "channel_id": CHANNEL_ID,
            "count": len(posts),
            "posts": posts
        }

    finally:
        await client.disconnect()
