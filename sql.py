import mysql.connector
import json
# from geopy import distance


class Sql:
    def __init__(self) -> None:
        self.connect = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="flight_game",
            user="root",
            password="metropolia",
            autocommit=True,
        )

    # Tiedon tuonti tietokannasta
    def pull(self, sql_code: str) -> list:
        cursor = self.connect.cursor()

        cursor.execute(sql_code)
        result = cursor.fetchall()

        if not result:
            print("-ERROR in sql_pull-")

        return result

    # Tiedon vienti tietokantaan
    def push(self, sql_code: str) -> int:
        cursor = self.connect.cursor()

        cursor.execute(sql_code)

        if cursor.rowcount <= 0:
            print("-ERROR in sql_push-")

        return cursor.rowcount

    # Kirjautumisfunktio
    def login(self, username: str, pin_code: str) -> str:
        # Kaikki käyttäjätunnukset ovat pienellä kirjoitettuja
        username = username.lower()

        # Haetaan käyttäjänimen ja PIN-koodin mukaan käyttäjä
        sql = "select screen_name, location from game "
        sql += f"where screen_name = '{username}' and passcode = '{pin_code}';"

        # Vedetään käyttäjätiedot tietokannasta.
        result = self.pull(sql)

        # Haku ei palauta tuloksia.
        if not result:
            return json.dumps({"ERROR": "Username not found, or PIN code was wrong."})
        else:
            return json.dumps({"name": result[0][0], "location": result[0][1]})

    def register(self, username: str, pin_code: str) -> str:
        # Kaikki käyttäjätunnukset ovat pienellä kirjoitettuja
        username = username.lower()

        # Tarkistetaan, onko käyttäjänimi 30 merkkiä tai alle
        if len(username) > 30:
            return json.dumps({"result": "Username too long."})
        # Tarkistetaan, onko PIN-koodi numeroita
        if not pin_code.isdigit() and len(pin_code) != 4:
            return json.dumps({"result": "PIN code error."})

        sql = "insert into game (location, screen_name, passcode) "
        sql += f"values ('EFHK', '{username}', {int(pin_code)})"

        # Pusketaan uuden käyttäjän tiedot tietokantaan.
        result = self.push(sql)

        if result <= 0:
            return json.dumps({"result": "Error storing credentials."})
        else:
            return json.dumps({"result": "Registration successful!"})

    def coordinates(self, start: str, end: str) -> None:
        return
