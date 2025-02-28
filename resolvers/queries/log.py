from ariadne import QueryType
from db import get_db

query = QueryType()

@query.field("logs")
async def resolve_logs(_, info, modelType, modelId):
    db = get_db()
    logs = list(db.logs.find({"model_type": modelType, "model_id": modelId}))
    for log in logs:
        log["id"] = str(log["_id"])
        del log["_id"]
        if "previous_data" in log and log["previous_data"] is None:
            log["previous_data"] = ""
    return logs