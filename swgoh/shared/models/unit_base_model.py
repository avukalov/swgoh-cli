from rich.text import Text

class UnitBase:

    name: str | Text
    gp: int | Text
    stars: int | Text
    gear: int | Text
    level: int | Text

    def __init__(self) -> None:
        pass