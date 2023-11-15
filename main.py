import random


DEST_ICAO = {
    "EFHK": 1,  # Helsinki
    "ESSA": 11,  # Ruotsi (HUOM Eka kiekka)
    "ENGM": 12,  # Norja
    "EVRA": 13,  # Latvia
    "EKCH": 14,  # Tanska
    "EYVI": 15,  # Liettua
    "EPWA": 21,  # Puola (HUOM Toka kierros)
    "EDDB": 22,  # Saksa
    "EHAM": 23,  # Alankomaat
    "LZIB": 24,  # Slovakia
    "LKPR": 25,  # Tsekki
    "LOWW": 31,  # Itävalta (HUOM Kolmas kierros)
    "LHBP": 32,  # Unkari
    "EBBR": 33,  # Belgia
    "LYBE": 34,  # Serbia
    "LDZA": 35,  # Kroatia
    "LSZH": 41,  # Sveitsi (HUOM Neljäs kierros)
    "LIRN": 42,  # Italia
    "LFPO": 43,  # Ranska
    "EGLL": 44,  # UK
    "EIDW": 45,  # Irlanti
    "LEBL": 51,  # Espanja (HUOM Viides kierros)
    "LPPT": 52,  # Portugali
    "GMMX": 53,  # Marokko
    "HECA": 54,  # Egypti
    "GCLP": 55,  # Gran Canaria
}


class Player:
    def __init__(
        self, name: str, money: int = 1000, location: str = "EFHK", emissions: int = 0
    ) -> None:
        self.name: str = name
        self.money: int = money
        self.location: str = location
        self.emissions: int = emissions
        self.can_travel: bool = True

    def fly(self, destination: str, price: int) -> None:
        # Laske lennon emissiot ja hinta
        # Varmista onko lentokohde oikea
        # if

        self.location = destination
        self.money -= price
        # self.emissions += emissiot lennosta

    def work(self, workplace: str) -> None:
        # Jos annettu työpaikka kusee
        if workplace not in ["burger", "exchange", "flower"]:
            return

        self.money += 175

    def update(self) -> dict:
        return {
            "name": self.name,
            "money": self.money,
            "location": self.location,
            "emissions": self.emissions,
        }


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
        icaos: list = list(DEST_ICAO)

        self.destination_list: list = []

        for x in range(1, 25, 5):
            rand: int = random.randint(0, 4)
            self.destination_list.append(icaos[x + rand])

        # Laske emissiot olemassa olevien lentokenttien perusteella


class World:
    # Kun tarvitaan ICAO-koodi ja numero
    def airport(self, icao: str) -> tuple[int, str]:
        # Palauttaa halutun ICAOn ja indeksinumeron
        return (DEST_ICAO[icao], icao)

    # - Funktio palauttaa listan kaikista pelaajalle
    # mahdollisista lentokohteista.
    def possible_locations(self, current: str, can_travel: bool) -> list:
        # Lista, jossa kaikki ICAO-koodit DEST_ICAO-sanakirjasta
        icaos: list = list(DEST_ICAO)
        # Pelaajan tämänhetkinen sijainti numerona
        cur: int = DEST_ICAO[current]
        # - Testataan pelaajan DEST_ICAO-arvonumeroa, jotta
        # voidaan asettaa oikeat rajat palautettavalle
        # listalle.
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
        # - Rakennetaan viiden sijainnin lista, jonka
        # indeksit edellinen ehtopuu on määrittänyt.
        return [icaos[x] for x in range(s, e)]


rotta = Rotta()

print(rotta.destination_list)
