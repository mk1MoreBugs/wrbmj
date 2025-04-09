import asyncio
import datetime

from redis.asyncio.client import Redis

from app.api.utils.redis_utils import set_note_in_redis, get_note_in_redis
from app.models.notes import NoteOutInDetailed


def test__get_note_in_redis__set_note_in_redis_and_get_it_in_redis__return_note_model(redis: Redis):
    note_id = 1
    test_note = NoteOutInDetailed(
        id=note_id,
        last_update=datetime.datetime.now(),
        note_content="note content",
        title_name="title name",
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    loop.run_until_complete(set_note_in_redis(redis=redis, note_id=note_id, note_id_detailed=test_note))
    note_coroutine = get_note_in_redis(redis=redis, note_id=note_id)
    note: NoteOutInDetailed = loop.run_until_complete(note_coroutine)

    assert note.note_content == test_note.note_content
    assert note.id == test_note.id
    assert note.last_update == test_note.last_update
    assert note.title_name == test_note.title_name


def test__get_note_in_redis__get_note_with_not_exist_id__return_none(redis: Redis):
    note_id = 0

    note_coroutine = get_note_in_redis(redis=redis,note_id=note_id)

    note: NoteOutInDetailed = asyncio.run(note_coroutine)

    assert note is None
