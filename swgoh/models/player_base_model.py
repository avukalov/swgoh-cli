from rich.text import Text
from swgoh.models import UnitBase


class PlayerBase:
    id: str
    name: str | Text
    allyCode: int | Text | None
    roster: list[UnitBase] | None
    gp: int | Text

    def __init__(self) -> None:
        pass