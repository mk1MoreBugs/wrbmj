from app.models.notes import NoteOutInDetailed

from redis.asyncio.client import Redis


PREFIX_STR = "note_id_"


async def get_note_in_redis(
        redis: Redis,
        note_id: int,
) -> NoteOutInDetailed | None:
    note_id_in_redis = PREFIX_STR + str(note_id)
    note_id_detailed_bytes: bytes = await redis.get(note_id_in_redis)
    if note_id_detailed_bytes is None:
        return None
    note_id_detailed_json = note_id_detailed_bytes.decode()
    note_in_detailed = NoteOutInDetailed.model_validate_json(note_id_detailed_json)
    return note_in_detailed


async def set_note_in_redis(
        redis: Redis,
        note_id: int,
        note_id_detailed: NoteOutInDetailed,
) -> None:
    note_id_in_redis = PREFIX_STR + str(note_id)

    note_id_detailed_json = note_id_detailed.model_dump_json()
    note_id_detailed_bytes = note_id_detailed_json.encode()
    await redis.set(note_id_in_redis, note_id_detailed_bytes)
