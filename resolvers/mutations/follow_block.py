from ariadne import MutationType
from db import get_db
from models.follow_block import FollowBlock
from datetime import datetime, UTC
from bson import ObjectId
from utils import json_serialize

mutation = MutationType()

@mutation.field("createFollowBlock")
async def resolve_create_follow_block(_, info, followerId, followingId, action):
    db = get_db()
    try:
        follower_id_obj = ObjectId(followerId)
        following_id_obj = ObjectId(followingId)
        follower = db.vendors.find_one({"_id": follower_id_obj})
        following = db.vendors.find_one({"_id": following_id_obj})
        if not follower:
            raise ValueError(f"Follower Vendor with ID {followerId} not found")
        if not following:
            raise ValueError(f"Following Vendor with ID {followingId} not found")
        if action not in ["follow", "block"]:
            raise ValueError("Action must be 'follow' or 'block'")
    except ValueError as e:
        raise ValueError(str(e))

    existing = db.follow_blocks.find_one({"follower_id": followerId, "following_id": followingId, "action": action})
    if existing:
        raise ValueError(f"Relation {action} already exists between {followerId} and {followingId}")

    follow_block = FollowBlock(
        follower_id=followerId,
        following_id=followingId,
        action=action,
        created_at=datetime.now(UTC).isoformat()
    )
    result = db.follow_blocks.insert_one(follow_block.dict())
    follow_block_id = str(result.inserted_id)
    follow_block.id = follow_block_id

    if action == "follow":
        db.vendors.update_one({"_id": follower_id_obj}, {"$inc": {"following_count": 1}})
        db.vendors.update_one({"_id": following_id_obj}, {"$inc": {"followers_count": 1}})
    elif action == "block":
        db.vendors.update_one({"_id": follower_id_obj}, {"$push": {"blocked_vendors": followingId}})

    from models.log import Log
    log = Log(
        model_type="FollowBlock",
        model_id=follow_block_id,
        action="create",
        changed_by=followerId,
        changed_at=datetime.now(UTC).isoformat(),
        new_data=json_serialize(follow_block.dict())
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})

    follow_block_dict = follow_block.__dict__
    follow_block_dict["id"] = follow_block_id
    return follow_block_dict

@mutation.field("deleteFollowBlock")
async def resolve_delete_follow_block(_, info, followBlockId):
    db = get_db()
    print(f"Attempting to delete follow_block with ID: {followBlockId}")  # دیباگ
    try:
        follow_block_id_obj = ObjectId(followBlockId)
        follow_block = db.follow_blocks.find_one({"_id": follow_block_id_obj})
        print(f"Found follow_block: {follow_block}")  # دیباگ
        if not follow_block:
            raise ValueError(f"FollowBlock with ID {followBlockId} not found")
    except ValueError as e:
        print(f"Error: {str(e)}")  # دیباگ
        raise ValueError(f"Invalid followBlockId format or not found: {followBlockId}")

    old_data = follow_block.copy()
    result = db.follow_blocks.delete_one({"_id": follow_block_id_obj})
    print(f"Delete result: {result.deleted_count}")  # دیباگ

    follower_id_obj = ObjectId(follow_block["follower_id"])
    following_id_obj = ObjectId(follow_block["following_id"])
    if follow_block["action"] == "follow":
        db.vendors.update_one({"_id": follower_id_obj}, {"$inc": {"following_count": -1}})
        db.vendors.update_one({"_id": following_id_obj}, {"$inc": {"followers_count": -1}})
    elif follow_block["action"] == "block":
        db.vendors.update_one({"_id": follower_id_obj}, {"$pull": {"blocked_vendors": follow_block["following_id"]}})

    from models.log import Log
    log = Log(
        model_type="FollowBlock",
        model_id=followBlockId,
        action="delete",
        changed_by=follow_block["follower_id"],
        changed_at=datetime.now(UTC).isoformat(),
        previous_data=json_serialize(old_data),
        new_data=""
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})

    old_data["id"] = str(old_data["_id"])
    del old_data["_id"]
    print(f"Returning deleted follow_block: {old_data}")  # دیباگ
    return old_data