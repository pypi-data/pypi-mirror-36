from typing import Optional


class Database:

    def __init__(self):
        pass

    def add_document(self, doc_id: str, doc: dict) -> None:
        raise NotImplementedError()

    def get_document_as_str(self, doc_id: str) -> Optional[str]:
        raise NotImplementedError()
