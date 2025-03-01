from ariadne import QueryType
from db import get_db
from bson import ObjectId

query = QueryType()

@query.field("stories")
async def resolve_stories(_, info, vendorId):
    db = get_db()
    print(f"Fetching stories for vendor_id: {vendorId}")
    stories = list(db.stories.find({"vendor_id": vendorId}))
    print(f"Raw stories from DB: {stories}")
    if not stories:
        print("No stories found, returning empty list")
        return []
    # فقط فیلدهای مورد نیاز رو دستی می‌سازیم تا از تداخل id دیتابیس جلوگیری کنیم
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
    print(f"Processed stories: {result}")
    return result