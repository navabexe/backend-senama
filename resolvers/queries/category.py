from ariadne import QueryType
from db import get_db
from bson import ObjectId

query = QueryType()

@query.field("categories")
async def resolve_categories(_, info):
    db = get_db()
    try:
        categories = list(db.categories.find())
        print("Categories from DB:", categories)  # برای دیباگ
        result = []
        for category in categories:
            category_dict = {
                "id": str(category["_id"]),
                "name": category.get("name", ""),  # مطمئن می‌شیم name همیشه مقدار داره
                "created_at": category.get("created_at", ""),
                "updated_at": category.get("updated_at", "")
            }
            result.append(category_dict)
        print("Categories result:", result)  # برای دیباگ
        return result  # همیشه یه لیست برمی‌گردونیم
    except Exception as e:
        print(f"Error fetching categories: {str(e)}")  # برای دیباگ
        return []  # در صورت خطا، لیست خالی برمی‌گردونیم

@query.field("subcategories")
async def resolve_subcategories(_, info, categoryId):
    db = get_db()
    try:
        category_id_obj = ObjectId(categoryId)
        subcategories = db.subcategories.find({"category_id": categoryId})
        return [{"id": str(s["_id"]), **{k: v for k, v in s.items() if k != "_id"}} for s in subcategories]
    except ValueError:
        raise ValueError(f"Invalid categoryId format: {categoryId}")