from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client import JournalAPI

class Base:
    def __init__(self, client: "JournalAPI"):
        self.client = client