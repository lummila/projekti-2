import random
import json


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
        self.name: str = name
        self.money: int = money
        self.location: str = location
        self.emissions: int = emissions
        self.can_travel: bool = True

    def fly(self, destination: str, price: int) -> tuple[str, str]:
        # Laske lennon emissiot ja hinta
        # Varmista onko lentokohde oikea
        if destination not in rotta.destination_list:
            self.can_travel = False

        start: str = self.location
        self.location = destination
        self.money -= price
        # self.emissions += emissiot lennosta

        return (start, self.location)

    def work(self, workplace: str) -> int:
        # Jos annettu työpaikka kusee
        if workplace not in ["burger", "exchange", "flower"]:
            return

        pay: int = 175 if self.can_travel else 200
        self.money += pay
        return pay

    def update(self) -> str:
        # Luodaan sanakirja pelaajan tämänhetkisistä tiedoista
        output: dict = {
            "name": self.name,
            "money": self.money,
            "location": self.location,
            "emissions": self.emissions,
            "possible_destinations": world.possible_locations(
                pelaaja.location, pelaaja.can_travel
            ),
        }

        # Tehdään sanakirjasta tekstiksi formatoitu JSON
        output_json: str = json.dumps(output)

        return output_json


class HelpMenu:
    def __init__(self, name: str) -> None:
        self.player_name: str = name

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
        # Tehdään DEST_ICAOsta lista
        icaos: list = list(DEST_ICAO)
        # Lista viidestä lentokentästä, jossa rotta on
        # käynyt (on viidennessä)
        self.destination_list: list = []
        # Tehdään flygariarvonta satunnaisten intien pohjalta
        # X on taso ja y satunnainen kenttä tasolta
        for x in range(1, 25, 5):
            y: int = random.randint(0, 4)
            # Lisätään icaos-listalta omaan listaan satunnaiset lentokentät
            self.destination_list.append(icaos[x + y])

        # Laske emissiot olemassa olevien lentokenttien
        # perusteella


class World:
    # Kun tarvitaan ICAO-koodi ja numero
    def airport(self, icao: str) -> tuple[int, str]:
        # Palauttaa halutun ICAOn ja indeksinumeron
        return (DEST_ICAO[icao], icao)

    # Funktio palauttaa listan kaikista pelaajalle
    # mahdollisista lentokohteista.
    def possible_locations(self, current: str, can_travel: bool) -> list:
        # Lista, jossa kaikki ICAO-koodit DEST_ICAO-sanakirjasta
        icaos: list = list(DEST_ICAO)
        # Pelaajan tämänhetkinen sijainti numerona
        cur: int = DEST_ICAO[current]
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
        return [icaos[x] for x in range(s, e)]

    def hint(self, current: str) -> None:
        # Vedä tietokannasta vinkki seuraavaa kohdetta varten
        pos_locs: list = world.possible_locations(current, pelaaja.can_travel)
        dest_hint: str = ""
        for x in rotta.destination_list:
            if x in pos_locs:
                dest_hint = x
                break

        # Hae SQL:stä vinkki
        return dest_hint


pelaaja: object = Player("Jari")
rotta: object = Rotta()
world: object = World()

print(rotta.destination_list)
print(world.hint("EKCH"))
