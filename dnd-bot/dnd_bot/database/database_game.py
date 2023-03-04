from sqlite3 import ProgrammingError

from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseGame:

    @staticmethod
    def add_game(token: str, id_host: int, game_state: str, campaign_name: str) -> int | None:
        """start game and add game to database
        :param token: lobby/game token (5 digit password)
        :param id_host: discord id of host
        :param game_state: string enum, initial value of added game is 'LOBBY'
        :param campaign_name: campaign  name
        :return:
            on success: game id, on failure: None
        """
        return DatabaseConnection.add_to_db('INSERT INTO public."Game" (token, id_host, game_state, campaign_name)'
        'VALUES (%s, %s, %s, %s)', (token, id_host, game_state, campaign_name))

    @staticmethod
    def start_game(id_game: int) -> None:
        """starts game
        :param id_game: database game id
        """
        DatabaseGame.update_game_state(id_game, 'ACTIVE')

    @staticmethod
    def update_game_state(id_game: int, game_state: str) -> None:
        """updates game state on the one provided
        """
        DatabaseConnection.cursor.execute('UPDATE public."Game" SET game_state = (%s) WHERE id_game = (%s)',
                                          (game_state, id_game))

        DatabaseConnection.connection.commit()

    @staticmethod
    def get_all_game_tokens():
        """returns all tokens currently existing in the database
        """
        DatabaseConnection.cursor.execute(f'SELECT token FROM public."Game"')
        tokens = DatabaseConnection.cursor.fetchall()
        DatabaseConnection.connection.commit()

        return [x[0] for x in tokens]

    @staticmethod
    def get_id_game_from_game_token(token: str) -> int | None:
        """returns database game id based on the token, None if the query fails
        """
        DatabaseConnection.cursor.execute(f'SELECT id_game FROM public."Game" WHERE token = (%s)', (token,))
        game_id = DatabaseConnection.cursor.fetchone()
        DatabaseConnection.connection.commit()

        if not game_id:
            return None

        return game_id

    @staticmethod
    def get_game_token_from_id_game(id_game: int) -> str | None:
        """returns game token based on database game id, None if the query fails
        """
        DatabaseConnection.cursor.execute(f'SELECT token FROM public."Game" WHERE id_game = (%s)', (id_game,))
        game_token = DatabaseConnection.cursor.fetchone()
        DatabaseConnection.connection.commit()

        if not game_token:
            return None

        return game_token

    @staticmethod
    def find_game_by_token(token: str) -> dict | None:
        """find game by token/password
        :param token: game token/password to find the game by
        :return: on success: dictionary containing game data - it's keys: 'id game' - database game id, 'token' - game token, 'id_host' -
        discord host id, 'id_campaign' - campaign id, 'game_state' - string enum, 'players' - list of players
        """

        DatabaseConnection.cursor.execute(f'SELECT * FROM public."Game" WHERE token = %s AND game_state != %s',
                                          (token, 'FINISHED'))
        game_tuple = DatabaseConnection.cursor.fetchone()

        if not game_tuple:
            return None

        DatabaseConnection.cursor.execute(f'SELECT * FROM public."User" WHERE id_game = {game_tuple[0]}')
        users_tuples = DatabaseConnection.cursor.fetchall()

        users = [{'id_user': user_tuple[0], 'id_game': user_tuple[1], 'discord_id': user_tuple[2]}
                 for user_tuple in users_tuples]

        return {'id_game': game_tuple[0], 'token': game_tuple[1], 'id_host': game_tuple[2],
                'id_campaign': game_tuple[3],
                'game_state': game_tuple[4], 'players': users}
