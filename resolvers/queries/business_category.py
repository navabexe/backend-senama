from ariadne import QueryType
from db import get_db

query = QueryType()


@query.field("businessCategories")
async def resolve_business_categories(_, info):
    db = get_db()
    categories = list(db.business_categories.find())
    result = []
    for category in categories:
        category_dict = {
            "id": str(category["_id"]),
            "name": category.get("name", ""),
            "created_at": category.get("created_at", ""),
            "updated_at": category.get("updated_at", "")
        }
        result.append(category_dict)
    return result