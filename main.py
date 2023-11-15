print("lmao")


class Player:
    def __init__(
        self, name: str, money: int = 1000, location: str = "EFHK", emissions: int = 0
    ) -> None:
        self.name = name
        self.money = money
        self.location = location
        self.emissions = emissions

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
    def __init__(self, d_l: list, o_e: int) -> None:
        self.destination_list = d_l
        self.optimal_emissions = o_e


class World:
    def __init__(self) -> None:
        pass
