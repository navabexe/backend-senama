from ariadne import MutationType
from db import get_db
from models.user_interaction import UserInteraction
from datetime import datetime, UTC

mutation = MutationType()

@mutation.field("trackInteraction")
async def resolve_track_interaction(_, info, targetType, targetId, action):
    db = get_db()
    interaction = UserInteraction(
        user_id="66f1a2b3c8d9e4f2b8c7d590",
        target_type=targetType,
        target_id=targetId,
        action=action,
        timestamp=datetime.now(UTC).isoformat()
    )
    result = db.user_interactions.insert_one(interaction.dict())
    interaction_id = str(result.inserted_id)
    interaction.id = interaction_id
    return interaction.__dict__