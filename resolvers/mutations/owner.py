from ariadne import MutationType
from db import get_db
from models.owner import Owner
from datetime import datetime, UTC
from bson import ObjectId

from utils import json_serialize

mutation = MutationType()


@mutation.field("createOwner")
async def resolve_create_owner(_, info, firstName, lastName, phone):
    db = get_db()
    owner = Owner(
        first_name=firstName,
        last_name=lastName,
        phone=phone,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    result = db.owners.insert_one(owner.dict())
    owner_id = str(result.inserted_id)
    owner.id = owner_id
    return owner.__dict__


@mutation.field("updateOwner")
async def resolve_update_owner(_, info, ownerId, firstName=None, lastName=None, phone=None, bio=None, avatarUrls=None,
                               phones=None, birthdate=None, gender=None, languages=None):
    db = get_db()
    try:
        owner_id_obj = ObjectId(ownerId)
        owner = db.owners.find_one({"_id": owner_id_obj})
        if not owner:
            raise ValueError(f"Owner with ID {ownerId} not found")
    except ValueError:
        raise ValueError(f"Invalid ownerId format: {ownerId}")

    old_data = owner.copy()
    if firstName is not None:
        owner["first_name"] = firstName
    if lastName is not None:
        owner["last_name"] = lastName
    if phone is not None:
        owner["phone"] = phone
    if bio is not None:
        owner["bio"] = bio
    if avatarUrls is not None:
        owner["avatar_urls"] = avatarUrls
    if phones is not None:
        owner["phones"] = phones
    if birthdate is not None:
        owner["birthdate"] = birthdate
    if gender is not None:
        owner["gender"] = gender
    if languages is not None:
        owner["languages"] = languages
    owner["updated_at"] = datetime.now(UTC).isoformat()
    db.owners.update_one({"_id": owner_id_obj}, {"$set": owner})

    from models.log import Log
    log = Log(
        model_type="Owner",
        model_id=ownerId,
        action="update",
        changed_by=ownerId,
        changed_at=datetime.now(UTC).isoformat(),
        previous_data=json_serialize(old_data),
        new_data=json_serialize(owner)
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})
    owner["id"] = str(owner["_id"])
    del owner["_id"]
    return owner


@mutation.field("deleteOwner")
async def resolve_delete_owner(_, info, ownerId):
    db = get_db()
    try:
        owner_id_obj = ObjectId(ownerId)
        owner = db.owners.find_one({"_id": owner_id_obj})
        if not owner:
            raise ValueError(f"Owner with ID {ownerId} not found")
    except ValueError:
        raise ValueError(f"Invalid ownerId format: {ownerId}")

    old_data = owner.copy()
    db.owners.delete_one({"_id": owner_id_obj})
    from models.log import Log
    log = Log(
        model_type="Owner",
        model_id=ownerId,
        action="delete",
        changed_by=ownerId,
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