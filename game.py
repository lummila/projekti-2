import random
import math
from sql import Sql

# Positiiviset sattumat
POS_COINCIDENCES = [
    "Nice! You found a 100€ bill on the airport floor.\n(100€ will be added to your account)",
    "You were helpful to a lost elderly. For the kind act he rewarded you with a 50€ bill!\n(50€ will be added to "
    "your account)",
    "Lucky you! The flight company made a mistake with your tickets. You'll be getting 80€ cashback!\n(80€ will be "
    "added to your account)",
    "There was a free seat at a more eco-friendly airplane!\n(10kg was removed from your emissions)",
    "The airplane took a shorter route. Emissions were 10kg less than expected.\n(10kg of emissions will be removed)",
    "Nothing of note has happened.",
]

# Negatiiviset sattumat
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

# Listat kaikkien kierrosten maista
# Ruotsi, Norja, Latvia, Tanska ja Liettua
ROUND_1 = ["ESSA", "ENGM", "EVRA", "EKCH", "EYVI"]
# Puola, Saksa, Alankomaat, Slovakia, Tsekki
ROUND_2 = ["EPWA", "EDDB", "EHAM", "LZIB", "LKPR"]
# Itävalta, Unkari, Belgia, Serbia, Kroatia
ROUND_3 = ["LOWW", "LHBP", "EBBR", "LYBE", "LDZA"]
# Sveitsi, Italia, Ranska, UK, Irlanti
ROUND_4 = ["LSZH", "LIRN", "LFPO", "EGLL", "EIDW"]
# Espanja, Portugali, Marokko, Egypti, Gran Canaria
ROUND_5 = ["LEBL", "LPPT", "GMMX", "HECA", "GCLP"]


# Rotan konstruktori, perii Sql:n tietokantahakuja varten.
class Rotta(Sql):
    def __init__(self) -> None:
        # Tämä tuottaa .connect ominaisuuden, joka on SQL-yhteyden käynnistys.
        Sql.__init__(self)
        # Lista viidestä lentokentästä, jossa rotta on käynyt (on viidennessä).
        # Tehdään flygariarvonta satunnaisten intien pohjalta X on taso ja y satunnainen kenttä tasolta.
        self.rotta_destination_list: list = [
            ROUND_1[random.randint(0, 4)],
            ROUND_2[random.randint(0, 4)],
            ROUND_3[random.randint(0, 4)],
            ROUND_4[random.randint(0, 4)],
            ROUND_5[random.randint(0, 4)],
        ]
        # Laske emissiot olemassa olevien lentokenttien perusteella.
        self.rotta_emissions: int = 0

        # Käydään läpi jokainen elementti rotta_destination_listissä ja lasketaan näiden välisten lentojen yhteisemissiot.
        for port in range(len(self.rotta_destination_list) - 1):
            emission = self.flight(
                self.rotta_destination_list[port], self.rotta_destination_list[port + 1]
            )

            # Lisätään joka kierroksella yhden lennon emissiot kokonaismäärään.
            self.rotta_emissions += emission * 115


# Pelaajan luokka, joka perii Rotan ja Sql:n. Sisältää kaikki ominaisuudet ja metodit pelin pelausta varten.
class Player(Rotta):
    connection_id = 0

    def __init__(self) -> None:
        # Luo self.rotta_emissions ja self.rotta_destination_list
        Rotta.__init__(self)
        # Käyttäjätunnuksen nimi
        self.name = ""
        # Rahamäärä, aina alussa 1000 €
        self.money = 1000
        # Alkusijainti, Helsinki-Vantaa eli EFHK
        self.location = "EFHK"
        # Tuotetut emissiot, aina 0 aluksi.
        self.emissions = 0
        # Voiko pelaaja matkustaa seuraavan tason lentokentille, boolean.
        self.can_travel = True
        # Pelaajan kierrokset, jos näitä on 10, peli päättyy.
        self.round = 1

    # Lentofunktio, siirtää pelaajan paikasta A paikkaan B.
    def fly(self, destination: str):
        # Varmista onko lentokohde oikeaan suuntaan.
        if destination not in self.rotta_destination_list:
            self.can_travel = False
        else:
            self.can_travel = True

        # Laske lennon emissiot ja hinta
        kilometers = self.flight(self.location, destination)

        # Lennon hinta, 100 € + (etäisyys jaettuna viidellätoista)
        price = math.floor(100 + kilometers / 15)
        # Lennon emissiot kiloina, kilometrit * 115 / 1000
        emissions = math.floor(kilometers * 115 / 1000)

        # Jos pelaajalla ei ole tarpeeksi rahaa, metodi päättyy ja palauttaa False.
        if self.money < price:
            return False

        # Jos kaikki on kunnossa, päivitetään pelaajan tiedot ja palautetaan True.
        self.location = destination
        self.money -= price
        self.emissions += emissions
        self.round += 1

        return True

    # Työskentelymetodi, lisätään pelaajalle rahaa ja yksi kierros. Ei varsinaisesti tarvitse palauttaa mitään.
    def work(self) -> int:
        self.money += 175
        self.round += 1
        return self.money

    # Palauttaa sanakirjan, jossa pelaajan tämänhetkinen tilanne.
    def update(self) -> dict:
        # Listataan pelaajalle mahdolliset lentokohteet
        destinations = self.possible_locations(self.location, self.can_travel)

        destinations_dict = {}
        for i in range(len(destinations)):
            destinations_dict[destinations[i]] = self.airport_info(destinations[i])

        # Luodaan sanakirja pelaajan tämänhetkisistä tiedoista
        return {
            "name": self.name,
            "money": self.money,
            "location": self.airport_info(self.location),
            "emissions": self.emissions,
            "possible_destinations": destinations_dict,
            "hint": self.hint(),
            "round": self.round,
            "coincidence": "Nothing of note has happened.",
        }

    # Funktio palauttaa listan kaikista pelaajallemahdollisista lentokohteista.
    def possible_locations(self, current: str, can_travel: bool) -> list:
        # Käydään läpi jokainen lista ja palautetaan oikea lista mahdollisia kohdemaita
        if current in ROUND_1:
            return ROUND_2 if can_travel else ROUND_1
        elif current in ROUND_2:
            return ROUND_3 if can_travel else ROUND_2
        elif current in ROUND_3:
            return ROUND_4 if can_travel else ROUND_3
        elif current in ROUND_4:
            return ROUND_5 if can_travel else ROUND_4
        elif current in ROUND_5:
            return ROUND_5
        else:
            return ROUND_1

    def hint(self):
        # Vedä tietokannasta vinkki seuraavaa kohdetta varten
        pos_locs = self.possible_locations(self.location, self.can_travel)
        dest_hint = ""
        for x in self.rotta_destination_list:
            if x in pos_locs:
                dest_hint = x
                break

        # Hae SQL:stä vinkki ja palauta se tekstinä
        return self.pull_hint(dest_hint)

    # Katsoo pelaajan tilanteen ja arpoo sattuman tapahtuvaksi.
    def coincidence(self, positive: bool):
        # Painoarvot positiivisille ja negatiivisille
        weights = [80, 20] if positive else [20, 80]
        # Valitsee yhden tekstin annetuilla painoarvoilla kahdesta listasta.
        choice = random.choice(
            random.choices([POS_COINCIDENCES, NEG_COINCIDENCES], weights=weights)[0]
        )
        # print(choice)

        # Käy läpi molemmat listat löytääkseen oikean tekstin, ja tekee operaation sen perusteella.
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
        # Palauttaa tekstin.
        return choice

    # Peli päättyy
    def game_over(self):
        # Lasketaan viimeiset pisteet
        final_score = math.floor(
            self.money * (10 - self.round if self.round < 10 else 1)
            + (self.rotta_emissions - self.emissions) / 1000
        )

        # Pusketaan tietokantaan joko nolla tai pelaajan pisteet
        result = self.push_score(self.name, final_score if final_score > 0 else 0)
        # Result palauttaa booleanin onnistumisen mukaan
        if result:
            return final_score
        else:
            return False
