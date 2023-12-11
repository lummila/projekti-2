import mysql.connector
from geopy import distance


class Sql:
    def __init__(self) -> None:
        """"
        self.connect = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="velkajahti",
            user="root",
            password="metropolia",
            autocommit=True,
        )

    def __init__(self) -> None:
        self.connect = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="velkajahti22",
            user="root",
            password="",
            autocommit=True,
        )"""
    def __init__(self) -> None:
        self.connect = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="velkajahti",
            user="root",
            password="Challenger-1971",
            autocommit=True,
        )



    # Tiedon tuonti tietokannasta
    def pull(self, sql_code: str):
        cursor = self.connect.cursor()
        cursor.execute(sql_code)
        result = cursor.fetchall()

        return result

    # Tiedon vienti tietokantaan
    def push(self, sql_code: str) -> int:
        cursor = self.connect.cursor()
        cursor.execute(sql_code)

        return cursor.rowcount

    # Kirjautumisfunktio
    def login(self, username: str, pin_code: str):
        # Kaikki käyttäjätunnukset ovat isolla kirjoitettuja
        username = username.upper()

        # Haetaan käyttäjänimen ja PIN-koodin mukaan käyttäjä
        sql = "select screen_name, location, passcode from game "
        sql += f"where screen_name = '{username}' and passcode = '{pin_code}';"

        # Vedetään käyttäjätiedot tietokannasta.
        result = self.pull(sql)

        # Jos haku ei palauta tuloksia.
        if not result:
            return False
        else:
            # SQL-luokalla ei ole name-ominaisuutta, tämä on Player-luokalla, jonka se muokkaa
            self.name = username
            return True

    # Rekisteröi uuden käyttäjän tietokantaan
    def register(self, username: str, pin_code: str):
        # Kaikki käyttäjätunnukset ovat isolla kirjoitettuja
        username = username.upper()

        # Ensin tarkistetaan, onko tietokannassa jo samanniminen käyttäjä
        sql = f"select screen_name from game where screen_name = '{username}'"
        result = self.pull(sql)

        if result:
            return False

        # Jos ei ole, tallennetaan uuden käyttäjän tiedot tietokantaan
        sql = "insert into game (location, screen_name, passcode) "
        sql += f"values ('EFHK', '{username}', {int(pin_code)})"

        # Pusketaan uuden käyttäjän tiedot tietokantaan.
        self.push(sql)

        # SQL-luokalla ei ole name-ominaisuutta, tämä on Player-luokalla, jonka se muokkaa
        self.name = username
        return True

    # Palauttaa listan, missä listat alku- ja kohdemaan koordinaateista ja lennon pituuden kilometreissä
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

            # Lisätään locationList-listaan tuple, jossa koordinaatit
            coord_list.append(result[0])

        kilometers = distance.distance(coord_list[0], coord_list[1]).km
        # Palautetaan koordinaatit ja lennon matka kilometreissä
        return coord_list, kilometers

    # Vetää hint-pöydästä pyydetyn kohteen vinkin
    def pull_hint(self, icao: str):
        sql = "select hint from hints "
        sql += f"where ident = '{icao}'"

        result = self.pull(sql)
        # Palauttaa vinkin tekstinä
        return result[0][0]

    # Palauttaa lentokentän nimen, maan nimen ja listan, missä koordinaatit
    def airport_info(self, icao: str):
        sql = "select airport.name, country.name, latitude_deg, longitude_deg from airport, country "
        sql += f"where airport.ident = '{icao}' and airport.iso_country = country.iso_country;"

        result = self.pull(sql)

        return {
            "airport_name": result[0][0],
            "country_name": result[0][1],
            "coordinates": [result[0][2], result[0][3]],
        }

    # Palauttaa max. 10 riviä huippupisteitä laskevassa järjestyksessä
    def high_score(self):
        sql = "select screen_name, points from goal order by points desc limit 10;"

        # Lista tupleja, joissa nimi ja pisteet
        return self.pull(sql)

    # Palauttaa max. 10 riviä huippupisteitä pyydetyltä pelaajalta laskevassa järjestyksessä
    def personal_high_score(self, username: str):
        sql = "select screen_name, points from goal "
        sql += f"where screen_name = '{username}' order by points desc limit 10;"

        # Lista tupleja, joissa nimi ja pisteet
        return self.pull(sql)

    # Pelin päätyttyä pelaajan huippupisteet tallennetaan, palauttaa True
    def push_score(self, username: str, points: int):
        sql = "insert into goal (screen_name, points) "
        sql += f"values ('{username}', {points});"

        self.push(sql)
        return True
