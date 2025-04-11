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
    return note_bytes_to_model(note_bytes=note_id_detailed_bytes)


def note_bytes_to_model(note_bytes: bytes) -> NoteOutInDetailed:
    note_json: str = note_bytes.decode()
    return NoteOutInDetailed.model_validate_json(note_json)


async def set_note_in_redis(
        redis: Redis,
        note_id: int,
        note_in_detailed: NoteOutInDetailed,
) -> None:
    note_id_in_redis = PREFIX_STR + str(note_id)
    note_id_detailed_bytes = note_model_to_bytes(note_model=note_in_detailed)

    await redis.set(note_id_in_redis, note_id_detailed_bytes)


def note_model_to_bytes(note_model: NoteOutInDetailed) -> bytes:
    note_json = note_model.model_dump_json()
    return note_json.encode()


async def get_and_delete_note_in_redis(
        redis: Redis,
        note_id: int,
) -> NoteOutInDetailed:
    note_id_in_redis = PREFIX_STR + str(note_id)
    note_id_detailed_bytes: bytes = await redis.getdel(note_id_in_redis)
    return note_bytes_to_model(note_bytes=note_id_detailed_bytes)
