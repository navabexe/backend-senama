from ariadne import QueryType
from db import get_db

query = QueryType()


@query.field("follows")
async def resolve_follows(_, info, followerId):
    db = get_db()
    follows = list(db.follow_blocks.find({"follower_id": followerId, "action": "follow"}))
    if not follows:
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
    return result


@query.field("blocks")
async def resolve_blocks(_, info, followerId):
    db = get_db()
    blocks = list(db.follow_blocks.find({"follower_id": followerId, "action": "block"}))
    if not blocks:
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
    return result