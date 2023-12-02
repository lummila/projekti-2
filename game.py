import random
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

POS_COINCIDENCES = [
    "Nice! You found a 100 € bill on the airport floor.\n(100 € will be added to your account)",
    "You were helpful to a lost elderly. For the kind act he rewarded you with a 50 € bill!\n(50 € will be added to "
    "your account)",
    "Lucky you! The flight company made a mistake with your tickets. You'll be getting 80 € cashback!\n(80 € will be "
    "added to your account)",
    "There was a free seat at a more eco-friendly airplane!\n(10 kg was removed from your emissions)",
    "The airplane took a shorter route. Emissions were 10 kg less than expected.\n(10 kg of emissions will be removed)",
    "Nothing of note has happened.",
]

NEG_COINCIDENCES = [
    "The airport lost your luggage... You'll have to wait one night at the airport.\n(One turn is used)",
    "Your flight was canceled, because of a raging storm. Your replacing flight leaves tomorrow morning.\n(One turn "
    "is used)",
    "You checked-in late to your flight. You'll have to pay a 100 € fee for the manual check-in.\n(100 € will be "
    "removed from your account)",
    "Your luggage was over weight. The fee for extra kilos is 50 €.\n(50 € will be removed from your account)",
    "The aircraft underestimated the flight's emissions. The emissions were 10 kg higher than expected.\n(10 kg of "
    "emissions will be added)",
    "Nothing of note has happened.",
]


class Rotta:
    def __init__(self) -> None:
        # Lista viidestä lentokentästä, jossa rotta on
        # käynyt (on viidennessä)
        self.rotta_destination_list: list = []
        # Tehdään flygariarvonta satunnaisten intien pohjalta
        # X on taso ja y satunnainen kenttä tasolta
        for x in range(1, 25, 5):
            y: int = random.randint(0, 4)
            # Lisätään icaos-listalta omaan listaan satunnaiset lentokentät
            self.destination_list.append(DEST_ICAO[x + y])

        # Laske emissiot olemassa olevien lentokenttien
        # perusteella
        self.rotta_emissions: int = 0

        for port in range(len(self.rotta_destination_list - 1)):
            emissions = Sql.flight(
                self.rotta_destination_list[port], self.rotta_destination_list[port + 1]
            )

            self.rotta_emissions += emissions[1] * 115


class Player(Sql, Rotta):
    def __init__(
        self,
        name: str,
        money: int = 1000,
        location: str = "EFHK",
        emissions: int = 0,
    ) -> None:
        Rotta.__init__(self)

        self.name = name
        self.money = money
        self.location = location
        self.emissions = emissions
        self.can_travel = True
        self.round = 0

    def fly(self, destination: str, price: int) -> tuple[str, str]:
        # Laske lennon emissiot ja hinta
        # Varmista onko lentokohde oikea
        if destination not in self.rotta_destination_list:
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
        for x in self.rotta_destination_list:
            if x in pos_locs:
                dest_hint = x
                break

        # HUOM: Testijuttu
        print(dest_hint)
        # Hae SQL:stä vinkki
        return self.pull_hint(dest_hint)

    def coincidence(self, positive=bool):
        weights = [80, 20] if positive else [20, 80]
        choice = random.choice(
            random.choices([POS_COINCIDENCES, NEG_COINCIDENCES], weights=weights)[0]
        )

        for index, text in enumerate(POS_COINCIDENCES):
            if choice == text:
                if index == 0:
                    self.money += 100
                elif index == 1:
                    self.money += 50
                elif index == 2:
                    self.money += 80
                elif index in [3, 4]:
                    self.emissions = (
                        self.emissions - 10000 if self.emissions >= 10000 else 0
                    )

        for index, text in enumerate(NEG_COINCIDENCES):
            if choice == text:
                if index in [0, 1]:
                    self.round += 1
                elif index == 2:
                    self.money = self.money - 100 if self.money >= 100 else 0
                elif index == 3:
                    self.money = self.money - 50 if self.money >= 50 else 0
                elif index == 4:
                    self.emissions += 10000
        return choice

    def rotta(self):
        return [self.rotta_destination_list, self.rotta_emissions]


pelaaja = Player("Jari")

print(pelaaja.rotta())