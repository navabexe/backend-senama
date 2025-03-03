from ariadne import QueryType
from db import get_db

query = QueryType()


@query.field("stories")
async def resolve_stories(_, info, vendorId):
    db = get_db()
    stories = list(db.stories.find({"vendor_id": vendorId}))
    if not stories:
        return []
    result = [
        {
            "id": str(s["_id"]),
            "vendor_id": s["vendor_id"],
            "media_url": s["media_url"],
            "description": s.get("description"),
            "link": s.get("link"),
            "tags": s.get("tags", [])
        } for s in stories
    ]
    return result