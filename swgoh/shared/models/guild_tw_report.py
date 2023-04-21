from rich.text import Text

class GuildTwReport(object):

    id: str | Text
    name: str | Text
    memberCount: int | Text
    gp: int | Text
    avgGp: int | Text
    gls: dict[str, dict[Text, int | Text]]
    ships: dict[str, dict[Text, int | Text]]
    overall: dict[str, int | Text]


    #TODO: CHANGE MODEL TO FIT DATABASE
    def __init__(self, guild: dict = None) -> None:
        if not guild:
            guild = {
                'id': '',
                'name': '',
                'memberCount': 0,
                'gp': 0,
                'avgGp': 0,
                'gls': {
                    "JABBATHEHUTT": { 'name': "JABBA", 'count': 0 },
                    "JEDIMASTERKENOBI": { 'name': "JMK", 'count': 0 },
                    "GRANDMASTERLUKE": { 'name': "JMLS", 'count': 0 },
                    "LORDVADER": { 'name': "LV", 'count': 0 },
                    "GLREY": { 'name': "REY", 'count': 0 },
                    "SITHPALPATINE": { 'name': "SEE", 'count': 0 },
                    "SUPREMELEADERKYLOREN": { 'name': "SLKR", 'count': 0 }
                },
                'ships': {},
                'overall': {
                    'characterGp': 0,
                    'shipGp': 0,
                    'medSkillRating': 0,
                    'medCurrArenaRank': 0,
                    'medCurrFleetArenaRank': 0
                }
            }

        for key in guild:
            setattr(self, key, guild[key])