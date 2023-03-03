from dnd_bot.database.database_user import DatabaseUser
from dnd_bot.logic.prototype.database_object import DatabaseObject


class User(DatabaseObject):
    """defines discord user"""

    def __init__(self, game_token: str = "", discord_id: int = 0, channel_id: int = 0, username: str = "", color: str = ""):
        ## TODO super().__init__(DatabaseUser.add_user())
        self.game_token = game_token
        self.discord_id = discord_id
        self.channel_id = channel_id
        self.username = username
        self.is_host = False
        self.is_ready = False
        self.color = color

    def __repr__(self):
        return f'<{self.username} id={self.discord_id} host={self.is_host}>'
