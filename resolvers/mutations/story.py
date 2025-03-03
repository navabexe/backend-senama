from datetime import datetime, UTC

from ariadne import MutationType
from bson import ObjectId

from core.utils import json_serialize
from db import get_db
from models.story import Story

mutation = MutationType()


@mutation.field("createStory")
async def resolve_create_story(_, info, vendorId, mediaUrl):
    db = get_db()
    vendor = db.vendors.find_one(
        {"_id": ObjectId(vendorId)})
    if not vendor:
        raise ValueError(f"Vendor with ID {vendorId} not found")

    story = Story(
        vendor_id=vendorId,
        media_url=mediaUrl,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    result = db.stories.insert_one(story.dict())
    story_id = str(result.inserted_id)
    story.id = story_id

    from models.log import Log
    log = Log(
        model_type="Story",
        model_id=story_id,
        action="create",
        changed_by=vendorId,
        changed_at=datetime.now(UTC).isoformat(),
        new_data=json_serialize(story.dict())
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})

    story_dict = story.__dict__
    story_dict["id"] = story_id
    return story_dict


@mutation.field("updateStory")
async def resolve_update_story(_, info, storyId, description=None, link=None, tags=None):
    db = get_db()
    try:
        story_id_obj = ObjectId(storyId)
        story = db.stories.find_one({"_id": story_id_obj})
        if not story:
            raise ValueError(f"Story with ID {storyId} not found")
    except ValueError:
        raise ValueError(f"Invalid storyId format: {storyId}")

    old_data = story.copy()
    if description is not None:
        story["description"] = description
    if link is not None:
        story["link"] = link
    if tags is not None:
        story["tags"] = tags
    story["updated_at"] = datetime.now(UTC).isoformat()

    db.stories.update_one({"_id": story_id_obj}, {"$set": story})

    from models.log import Log
    log = Log(
        model_type="Story",
        model_id=storyId,
        action="update",
        changed_by=story["vendor_id"],
        changed_at=datetime.now(UTC).isoformat(),
        previous_data=json_serialize(old_data),
        new_data=json_serialize(story)
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})

    story["id"] = str(story["_id"])
    del story["_id"]
    return story


@mutation.field("deleteStory")
async def resolve_delete_story(_, info, storyId):
    db = get_db()
    try:
        story_id_obj = ObjectId(storyId)
        story = db.stories.find_one({"_id": story_id_obj})
        if not story:
            raise ValueError(f"Story with ID {storyId} not found")
    except ValueError:
        raise ValueError(f"Invalid storyId format: {storyId}")

    old_data = story.copy()
    db.stories.delete_one({"_id": story_id_obj})

    from models.log import Log
    log = Log(
        model_type="Story",
        model_id=storyId,
        action="delete",
        changed_by=story["vendor_id"],
        changed_at=datetime.now(UTC).isoformat(),
        previous_data=json_serialize(old_data),
        new_data=""
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})

    old_data["id"] = str(old_data["_id"])
    del old_data["_id"]
    return old_data
