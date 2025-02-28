from ariadne import QueryType
from db import get_db

query = QueryType()

@query.field("interactions")
async def resolve_interactions(_, info, userId):
    db = get_db()
    interactions = db.user_interactions.find({"user_id": userId})
    return [{"id": str(i["_id"]), **{k: v for k, v in i.items() if k != "_id"}} for i in interactions]