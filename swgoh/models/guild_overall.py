

class GuildOverall(object):

    def __init__(self, guild: dict = None) -> None:
        if not guild:
            guild = {
                'name': '',
                'memberCount': 0,
                'gp': 0,
                'avgGp': 0,
                'gls': [],
                'ships': [],
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