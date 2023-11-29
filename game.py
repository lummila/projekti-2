import random
import json
from sql import Sql


DEST_ICAO = [
    "EFHK",  # Helsinki
    "ESSA",  # Ruotsi (HUOM Eka kiekka)
    "ENGM",  # Norja
    "EVRA",  # Latvia
    "EKCH",  # Tanska
    "EYVI",  # Liettua
    "EPWA",  # Puola (HUOM Toka kierros)
    "EDDB",  # Saksa
    "EHAM",  # Alankomaat
    "LZIB",  # Slovakia
    "LKPR",  # Tsekki
    "LOWW",  # Itävalta (HUOM Kolmas kierros)
    "LHBP",  # Unkari
    "EBBR",  # Belgia
    "LYBE",  # Serbia
    "LDZA",  # Kroatia
    "LSZH",  # Sveitsi (HUOM Neljäs kierros)
    "LIRN",  # Italia
    "LFPO",  # Ranska
    "EGLL",  # UK
    "EIDW",  # Irlanti
    "LEBL",  # Espanja (HUOM Viides kierros)
    "LPPT",  # Portugali
    "GMMX",  # Marokko
    "HECA",  # Egypti
    "GCLP",  # Gran Canaria
]


class Player:
    def __init__(
        self, name: str, money: int = 1000, location: str = "EFHK", emissions: int = 0
    ) -> None:
        self.name = name
        self.money = money
        self.location = location
        self.emissions = emissions
        self.can_travel = True

    def fly(self, destination: str, price: int) -> tuple[str, str]:
        # Laske lennon emissiot ja hinta
        # Varmista onko lentokohde oikea
        if destination not in rotta.destination_list:
            self.can_travel = False

        start = self.location
        self.location = destination
        self.money -= price
        # self.emissions += emissiot lennosta

        return (start, self.location)

    def work(self, workplace: str) -> int:
        # Jos annettu työpaikka kusee
        if workplace not in ["burger", "exchange", "flower"]:
            return

        pay = 175 if self.can_travel else 200
        self.money += pay
        return pay

    def update(self) -> dict:
        # Luodaan sanakirja pelaajan tämänhetkisistä tiedoista
        output = {
            "name": self.name,
            "money": self.money,
            "location": self.location,
            "emissions": self.emissions,
            "possible_destinations": self.possible_locations(
                self.location, self.can_travel
            ),
        }

        return output

    # Funktio palauttaa listan kaikista pelaajalle
    # mahdollisista lentokohteista.
    def possible_locations(self, current: str, can_travel: bool) -> list:
        # Pelaajan tämänhetkinen sijainti numerona
        cur = [i for i in range(len(DEST_ICAO)) if DEST_ICAO[i] == self.location][0]

        # - Testataan pelaajan DEST_ICAO-arvonumeroa, jotta
        # voidaan asettaa oikeat rajat palautettavalle
        # listalle mahdollisista lentomaista.
        # - Pelaaja-luokassa on can_travel-ominaisuus,
        # joka määrittää sen, voiko pelaaja edetä
        # seuraavan tason lentokentille, ja tämä funktio
        # testaa sen.
        if cur < 10:
            (s, e) = (1, 6)
        elif 10 < cur < 20:
            (s, e) = (6, 11) if can_travel else (1, 6)
        elif 20 < cur < 30:
            (s, e) = (11, 16) if can_travel else (6, 11)
        elif 30 < cur < 40:
            (s, e) = (16, 21) if can_travel else (11, 16)
        else:
            (s, e) = (21, 26) if can_travel else (16, 21)
        # Rakennetaan viiden sijainnin lista, jonka
        # indeksit edellinen ehtopuu on määrittänyt.
        icaos = [DEST_ICAO[x] for x in range(s, e)]

        for entry in icaos:
            return

    def hint(self, current: str) -> None:
        # Vedä tietokannasta vinkki seuraavaa kohdetta varten
        pos_locs = self.possible_locations(current, self.can_travel)
        dest_hint = ""
        for x in rotta.destination_list:
            if x in pos_locs:
                dest_hint = x
                break

        # HUOM: Testijuttu
        print(dest_hint)
        # Hae SQL:stä vinkki
        return sql.pull_hint(dest_hint)


class HelpMenu:
    def __init__(self, name: str) -> None:
        self.player_name = name

    def personal_score(self) -> None:
        pass

    def high_score(self) -> None:
        pass

    def rules(self) -> None:
        pass

    def continue_game(self) -> None:
        pass


class Rotta:
    def __init__(self) -> None:
        # Lista viidestä lentokentästä, jossa rotta on
        # käynyt (on viidennessä)
        self.destination_list: list = []
        # Tehdään flygariarvonta satunnaisten intien pohjalta
        # X on taso ja y satunnainen kenttä tasolta
        for x in range(1, 25, 5):
            y: int = random.randint(0, 4)
            # Lisätään icaos-listalta omaan listaan satunnaiset lentokentät
            self.destination_list.append(DEST_ICAO[x + y])

        # Laske emissiot olemassa olevien lentokenttien
        # perusteella


rotta = Rotta()
sql = Sql()

# print(rotta.destination_list)
# print(world.hint("EKCH"))

# print(sql.login(pelaaja.name, 1234))
