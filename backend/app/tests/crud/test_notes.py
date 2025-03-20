from datetime import datetime
from sqlmodel import Session

from app.crud.notes import get_note_by_id, create_note, get_notes_by_username
from app.models.notes import NotesInDb
from app.tests.utils.users import get_unique_username, create_test_user


def test__create_note__create_note_and_return_note_from_db__return_note(db: Session, unique_usernames: set[str]) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    test_user = create_test_user(db=db, username=username, plain_password="plain_password")
    test_note_content = "note content"
    test_note = NotesInDb(
        user_id=test_user.id,
        last_update=datetime.now(),
        noteContent=test_note_content,
        title_name="Title name",
    )

    create_note(session=db, note=test_note)

    test_note_in_db = get_note_by_id(session=db, note_id=test_note.id)
    assert test_note_in_db.id == test_note.id
    assert test_note_in_db.noteContent == test_note.noteContent
    assert test_note_in_db.title_name == test_note.title_name
    assert test_note_in_db.last_update == test_note.last_update


def test__get_note_by_id__get_note_by_non_existent_id__return_none(db: Session) -> None:
    test_note_in_db = get_note_by_id(session=db, note_id=100) # note_id=100 is non-existent
    assert test_note_in_db is None


def test__create_note__create_many_notes_and_return_notes_from_db__return_notes(db: Session, unique_usernames: set[str]) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    test_user = create_test_user(db=db, username=username, plain_password="plain_password")
    test_note_content = "note content"
    test_notes = [
        NotesInDb(
        user_id=test_user.id,
        last_update=datetime.now(),
        noteContent=f"{test_note_content}1",
        title_name="Title name",
        ),
        NotesInDb(
            user_id=test_user.id,
            last_update=datetime.now(),
            noteContent=f"{test_note_content}2",
            title_name="Title name",
        ),
        NotesInDb(
            user_id=test_user.id,
            last_update=datetime.now(),
            noteContent=f"{test_note_content}3",
            title_name="Title name",
        ),
    ]

    for note in test_notes:
        create_note(session=db, note=note)

    test_notes_by_username = get_notes_by_username(session=db, username=test_user.username)
    assert len(test_notes_by_username) == len(test_notes)


def test__create_note__create_note_for_many_users__return_notes_of_correct_user(db: Session, unique_usernames: set[str]) -> None:
    username1 = get_unique_username(unique_usernames=unique_usernames)
    test_user1 = create_test_user(db=db, username=username1, plain_password="plain_password")
    username2 = get_unique_username(unique_usernames=unique_usernames)
    test_user2 = create_test_user(db=db, username=username2, plain_password="plain_password")
    test_note_content = "note content"
    test_notes = [
        NotesInDb(
            user_id=test_user1.id,
            last_update=datetime.now(),
            noteContent=f"{test_note_content}1",
            title_name="Title name",
        ),
        NotesInDb(
            user_id=test_user2.id,
            last_update=datetime.now(),
            noteContent=f"{test_note_content}2",
            title_name="Title name",
        ),
        NotesInDb(
            user_id=test_user1.id,
            last_update=datetime.now(),
            noteContent=f"{test_note_content}3",
            title_name="Title name",
        ),
    ]

    for note in test_notes:
        create_note(session=db, note=note)

    test_notes_by_username1 = get_notes_by_username(session=db, username=test_user1.username)
    test_notes_by_username2 = get_notes_by_username(session=db, username=test_user2.username)
    assert len(test_notes_by_username1) == 2
    assert len(test_notes_by_username2) == 1
