import mysql.connector
import json
from geopy import distance


class Sql:
    def __init__(self) -> None:
        self.connect = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="velkajahti",
            user="root",
            password="metropolia",
            autocommit=True,
        )

    # Tiedon tuonti tietokannasta
    def pull(self, sql_code: str):
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
    def login(self, username: str, pin_code: str):
        # Kaikki käyttäjätunnukset ovat isolla kirjoitettuja
        username = username.upper()

        # Haetaan käyttäjänimen ja PIN-koodin mukaan käyttäjä
        sql = "select screen_name, location from game "
        sql += f"where screen_name = '{username}' and passcode = '{pin_code}';"

        # Vedetään käyttäjätiedot tietokannasta.
        result = self.pull(sql)

        # Haku ei palauta tuloksia.
        if not result:
            return -1
        else:
            return {"name": result[0][0], "location": result[0][1]}

    def register(self, username: str, pin_code: str) -> str:
        # Kaikki käyttäjätunnukset ovat isolla kirjoitettuja
        username = username.upper()

        # Tarkistetaan, onko käyttäjänimi 30 merkkiä tai alle
        if len(username) > 30:
            return json.dumps({"result": False, "info": "Username too long."})
        # Tarkistetaan, onko PIN-koodi numeroita
        if not pin_code.isdigit() and len(pin_code) != 4:
            return json.dumps({"result": False, "info": "PIN code error."})

        sql = "insert into game (location, screen_name, passcode) "
        sql += f"values ('EFHK', '{username}', {int(pin_code)})"

        # Pusketaan uuden käyttäjän tiedot tietokantaan.
        result = self.push(sql)

        if result <= 0:
            return json.dumps({"result": False, "info": "Error storing credentials."})
        else:
            return json.dumps({"result": True, "info": "Registration successful!"})

    def flight(self, start: str, end: str):
        # Lista, jossa kahdet koordinaatit
        coord_list = []

        # Kaksi eri hakua, aloitusmaan ja päämäärän etäisyyden selvittämiseksi.
        for x in range(2):
            sql = "select longitude_deg, latitude_deg from airport "
            # Jos x on 0, kyseessä on ensimmäinen haku, eli käytetään start-muuttujaa, ja toisella kerralla end-muuttujaa.
            sql += f"where ident = '{start if x == 0 else end}';"

            # SQL:n käyttö
            result = self.pull(sql)

            if not result:
                print("ERROR calculating coordinates in sql_coordinate_query()")
                return [-1, 0]
            else:
                # Lisätään locationList-listaan tuple, jossa koordinaatit
                coord_list.append(result[0])

        kilometers = distance.distance(coord_list[0], coord_list[1]).km
        # Palautetaan koordinaatit ja lennon matka kilometreinä
        return coord_list, kilometers

    def pull_hint(self, icao: str):
        sql = "select hint from hints "
        sql += f"where ident = '{icao}'"

        result = self.pull(sql)
        if not result:
            print("ERROR fetching hint in pull_hint()")
            return -1
        else:
            return result[0][0]

    def airport_info(self, icao: str):
        sql = "select airport.name, country.name, latitude_deg, longitude_deg "
        sql += f"where airport.ident = '{icao}' and airport.iso_country == country.iso_country;"

        result = self.pull(sql)
        if not result:
            print("ERROR fetching airport information in airport_info()")
            return -1

        return {
            "airport_name": result[0][0],
            "country_name": result[0][1],
            "coordinates": [result[0][2], result[0][3]],
        }
