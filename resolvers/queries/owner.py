from ariadne import QueryType
from db import get_db
from bson import ObjectId

query = QueryType()


@query.field("owner")
async def resolve_owner(_, info, ownerId):
    db = get_db()
    try:
        owner_id_obj = ObjectId(ownerId)
        owner = db.owners.find_one({"_id": owner_id_obj})
        if not owner:
            return None
    except ValueError:
        raise ValueError(f"Invalid ownerId format: {ownerId}")

    owner["id"] = str(owner["_id"])
    del owner["_id"]
    return owner