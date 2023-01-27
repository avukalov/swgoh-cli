from enum import Enum


# GuildReportKeys = Enum('GuildReportKeys'['TW', 'TB', 'RAID'])

class GuildReportKeys(Enum):
    TW = 0
    TB = 1
    RAID = 2


class TBKeys(Enum):
    DSHOTH = "TB_HOTH_IMPERIAL_RETALIATION"