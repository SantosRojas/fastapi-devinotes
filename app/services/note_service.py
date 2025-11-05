

from sqlmodel import Session

from app.models.note import Note
from app.models.share import ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.notes = NoteRepository(db)
        self.labels = LabelRepository(db)
        self.shares = ShareRepository(db)

    # Permisos

    def user_can_read(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.shares.has_note_share(note_id=note.id, user_id=user_id):
            return True

        label_ids = self.labels.list_label_ids_for_note(note.id)
        return self.shares.has_any_label_share(label_ids=label_ids, user_id=user_id)

    def user_can_edit(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.shares.has_note_share(note_id=note.id, user_id=user_id, role=ShareRole.EDIT):
            return True

        label_ids = self.labels.list_label_ids_for_note(note.id)
        return self.shares.has_any_label_share(label_ids=label_ids, user_id=user_id, role=ShareRole.EDIT)
