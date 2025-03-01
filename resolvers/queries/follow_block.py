from ariadne import QueryType
from db import get_db
from bson import ObjectId

query = QueryType()

@query.field("follows")
async def resolve_follows(_, info, followerId):
    db = get_db()
    print(f"Fetching follows for follower_id: {followerId}")  # دیباگ
    follows = list(db.follow_blocks.find({"follower_id": followerId, "action": "follow"}))
    print(f"Raw follows from DB: {follows}")  # دیباگ
    if not follows:
        print("No follows found, returning empty list")  # دیباگ
        return []
    result = [
        {
            "id": str(f["_id"]),
            "follower_id": f["follower_id"],
            "following_id": f["following_id"],
            "action": f["action"],
            "created_at": f["created_at"]
        } for f in follows
    ]
    print(f"Processed follows: {result}")  # دیباگ
    return result

@query.field("blocks")
async def resolve_blocks(_, info, followerId):
    db = get_db()
    print(f"Fetching blocks for follower_id: {followerId}")  # دیباگ
    blocks = list(db.follow_blocks.find({"follower_id": followerId, "action": "block"}))
    print(f"Raw blocks from DB: {blocks}")  # دیباگ
    if not blocks:
        print("No blocks found, returning empty list")  # دیباگ
        return []
    result = [
        {
            "id": str(b["_id"]),
            "follower_id": b["follower_id"],
            "following_id": b["following_id"],
            "action": b["action"],
            "created_at": b["created_at"]
        } for b in blocks
    ]
    print(f"Processed blocks: {result}")  # دیباگ
    return result