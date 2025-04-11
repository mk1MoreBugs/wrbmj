import time

from datetime import datetime
from sqlmodel import Session

from app.api.utils.note_utils import get_current_timestamp
from app.crud import notes
from app.models.notes import NoteInDb
from app.tests.utils.notes import create_test_note
from app.tests.utils.users import get_unique_username, create_test_user


def test__create_note__create_note_and_return_note_from_db__return_note(db: Session, unique_usernames: set[str]) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    test_user = create_test_user(db=db, username=username, plain_password="plain_password")
    test_note_content = "note content"
    test_note = NoteInDb(
        user_id=test_user.id,
        last_update=datetime.now(),
        note_content=test_note_content,
        title_name="Title name",
    )

    notes.create_note(session=db, note=test_note)

    test_note_in_db = notes.get_note_by_id(session=db, note_id=test_note.id)
    assert test_note_in_db.id == test_note.id
    assert test_note_in_db.note_content == test_note.note_content
    assert test_note_in_db.title_name == test_note.title_name
    assert test_note_in_db.last_update == test_note.last_update
    assert len(test_note_in_db.model_dump()) == 4


def test__get_note_by_id__get_note_by_non_existent_id__return_none(db: Session) -> None:
    test_note_in_db = notes.get_note_by_id(session=db, note_id=100) # note_id=100 is non-existent
    assert test_note_in_db is None


def test__create_note__create_many_notes_and_return_notes_from_db__return_notes(db: Session, unique_usernames: set[str]) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    test_user = create_test_user(db=db, username=username, plain_password="plain_password")
    test_note_content = "note content"
    test_notes = [
        NoteInDb(
        user_id=test_user.id,
        last_update=datetime.now(),
        note_content=f"{test_note_content}1",
        title_name="Title name",
        ),
        NoteInDb(
            user_id=test_user.id,
            last_update=datetime.now(),
            note_content=f"{test_note_content}2",
            title_name="Title name",
        ),
        NoteInDb(
            user_id=test_user.id,
            last_update=datetime.now(),
            note_content=f"{test_note_content}3",
            title_name="Title name",
        ),
    ]

    for note in test_notes:
        notes.create_note(session=db, note=note)

    test_notes_by_username = notes.get_notes_by_username(session=db, username=test_user.username)
    assert len(test_notes_by_username) == len(test_notes)


def test__create_note__create_note_for_many_users__return_notes_of_correct_user(db: Session, unique_usernames: set[str]) -> None:
    username1 = get_unique_username(unique_usernames=unique_usernames)
    test_user1 = create_test_user(db=db, username=username1, plain_password="plain_password")
    username2 = get_unique_username(unique_usernames=unique_usernames)
    test_user2 = create_test_user(db=db, username=username2, plain_password="plain_password")
    test_note_content = "note content"
    test_notes = [
        NoteInDb(
            user_id=test_user1.id,
            last_update=datetime.now(),
            note_content=f"{test_note_content}1",
            title_name="Title name",
        ),
        NoteInDb(
            user_id=test_user2.id,
            last_update=datetime.now(),
            note_content=f"{test_note_content}2",
            title_name="Title name",
        ),
        NoteInDb(
            user_id=test_user1.id,
            last_update=datetime.now(),
            note_content=f"{test_note_content}3",
            title_name="Title name",
        ),
    ]

    for note in test_notes:
        notes.create_note(session=db, note=note)

    test_notes_by_username1 = notes.get_notes_by_username(session=db, username=test_user1.username)
    test_notes_by_username2 = notes.get_notes_by_username(session=db, username=test_user2.username)
    assert len(test_notes_by_username1) == 2
    assert len(test_notes_by_username2) == 1


def test__get_notes_by_username__get_notes_by_username__return_empty_list(db: Session, unique_usernames: set[str]) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    test_user = create_test_user(db=db, username=username, plain_password="plain_password")

    test_notes_by_username = notes.get_notes_by_username(session=db, username=test_user.username)
    assert len(test_notes_by_username) == 0


def test__update_content_note_by_id__create_note_and_update_note_content__get_updated_field(db: Session, unique_usernames: set[str]) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    test_user = create_test_user(db=db, username=username, plain_password="plain_password")
    old_note_content = "note content"
    new_note_content = "new note content"
    test_note = create_test_note(
        db=db,
        user_id=test_user.id,
        note_content=old_note_content,
    )
    old_note_timestamp = test_note.last_update

    notes.update_content_note_by_id(
        session=db,
    note_id=test_note.id,
    note_text=new_note_content,
    timestamp=get_current_timestamp(),
    )
    time.sleep(0.25)  # so that there would be different timestamps

    assert test_note.note_content == new_note_content
    assert old_note_timestamp < test_note.last_update


def test__update_title_note_by_id__create_note_and_update_note_title__get_updated_field(db: Session, unique_usernames: set[str]) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    test_user = create_test_user(db=db, username=username, plain_password="plain_password")
    old_note_title = "note title"
    new_note_title = "new note title"
    test_note = create_test_note(
        db=db,
        user_id=test_user.id,
        note_content="note content",
        title_name=old_note_title,
    )
    old_note_timestamp = test_note.last_update

    notes.update_title_note_by_id(
        session=db,
    note_id=test_note.id,
    title_note=new_note_title,
    timestamp=get_current_timestamp(),
    )
    time.sleep(0.25)  # so that there would be different timestamps

    assert test_note.title_name == new_note_title
    assert old_note_timestamp < test_note.last_update



