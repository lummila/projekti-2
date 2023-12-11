"use strict";

// Pelaajan vinkki seuraavaan kohteeseen
const tutorial = document.querySelector("#next-hint");

// Elementtilista kaikista lentokenttänappuloista
const icaoButtons = document.querySelectorAll(".icao-button");

// Pelaajan viimeisin sattuma
const coincidence = document.querySelector("#given-coincidence");

// Pelaajan raha-, päästö- ja kierrostilanteet
const money = document.querySelector("#money");
const emissions = document.querySelector("#emissions");
const round = document.querySelector("#round");

// Työnappula, toimii myös jatka-nappulana
const workButton = document.querySelector("#work-button");

const map = L.map("map").setView([60.31, 24.94], 5);
const mapElement = document.querySelector("#map");
const markers = L.layerGroup();

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 16,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// PELILOGIIKAN KÄSITTELY
const gameLogic = {
  async fetchInfo() {
    try {
      //
      const response = await fetch("http://127.0.0.1:5000/update");
      const response_json = await response.json();

      return response_json;
    } catch (error) {
      console.error("Error updating game data", error);
      return error;
    }
  },
  async flyToSweden() {
    try {
      const response = await fetch("http://127.0.0.1:5000/fly?dest=ESSA");
      const response_json = await response.json();

      gameLogic.update();
    } catch (error) {
      console.error("gameLogic.update() failed", error);
    }
  },
  async reset() {
    try {
      const response = await fetch("http://127.0.0.1:5000/reset");
      if (response.status != 200) {
        return -1;
      }
      const response_json = await response.json();
    } catch (error) {
      console.log("gameLogic.reset() failed", error);
    }
  },
  async update() {
    const data = await this.fetchInfo();
    // HUOM VAIN KEHITYSTARPEISIIN
    console.log(data);

    markers.clearLayers();

    // Otetaan tuodusta datasta vain lentokentät-osio
    const airports = data.possible_destinations;

    // Käydään jokainen ICAO-nappula läpi ja sijoitetaan niihin oikeat tiedot
    icaoButtons.forEach((e, i) => {
      // Otetaan ylös tämänhetkisen iteraation ICAO-koodi
      const icao = Object.keys(airports)[i];
      // e on ICAO-nappula ja siihen syötetään teksti airports-objektista icao-koodin avulla
      e.textContent = `${airports[icao].airport_name}, ${airports[icao].country_name}`;
    });

    // Pelaajan tämänhetkinen sijainti
    const marker = L.marker(data.location.coordinates, {
      title: data.location.airport_name,
    });

    marker.bindPopup(data.location.airport_name);
    // Lisätään täppälistaan nykyinen sijainti
    markers.addLayer(marker);

    //Käydään läpi kaikki mahdollisten kohteiden koordinaatit ja laitetaan pisteet niiden päälle
    console.log(airports);
    for (const i in airports) {
      const dot = L.marker(airports[i].coordinates, {
        title: airports[i].airport_name,
      });
      dot.bindPopup(airports[i].airport_name);
      markers.addLayer(dot);
    }
    // Lisätään täpät karttaan
    map.addLayer(markers);
    // Sattumateksti
    coincidence.textContent = data.coincidence;
    // Rahamäärä
    money.textContent = data.money;
    // Emissiomäärä
    emissions.textContent = data.emissions;
    // Kierros
    round.textContent = data.round;
  },
};

gameLogic.update();
let stages = 0;

tutorial.textContent =
  "Welcome to the tutorial! In this short interactive demonstration, you will learn to play Velkajahti. We will go over flying to different countries and working for money. Press the 'Work' button to continue.";

workButton.addEventListener("click", () => {
  if (stages == 0) {
    stages++;

    tutorial.textContent =
      "During the game, you will receive hints about your next destination, which will be displayed where this text is. But now, I will assist you and tell you where to travel. We will go to Sweden. Press the button which reads: 'Stockholm-Arlanda Airport, Sweden'.";
  }
});

icaoButtons[0].addEventListener("click", async () => {
  if (stages == 1) {
    stages++;
    gameLogic.flyToSweden();
    tutorial.textContent =
      "Here we are, beautiful Sweden. You'll see that the flight cost money, increased your emission count and round count. If you reach 10 rounds without reaching the Rat, you lose the game! You may have new list of destinations, or not, depending on if you went the right location. Anyway, press 'Work' to continue.";
  }
});

workButton.addEventListener("click", () => {
  if (stages == 2) {
    stages++;
    tutorial.textContent =
      "Now it's time to work for a bit. If you now press the 'Work' button, you will be taken to a submenu that offers different options for a short-time gig. Doing work gives you money, but it will also spend one round, so use it wisely!";

    const workModal = document.querySelector("#work-modal");
    const workSpan = document.getElementsByClassName("close")[4];

    workButton.onclick = function () {
      // Piilotetaan kartta
      mapElement.classList.add("hidden");
      workModal.style.display = "block";
    };

    workSpan.onclick = function () {
      // Näytetään kartta taas
      mapElement.classList.remove("hidden");
      workModal.style.display = "none";
      tutorial.textContent =
        "That concludes the most important parts of the game. You seem a natural at this, so I'll leave the rest for you. You'll gain more experience through first-hand experience, os You can exit to the main menu by pressing the 'Exit' button.";
    };

    window.onclick = function (event) {
      if (event.target == workModal) {
        workModal.style.display = "none";
      }
    };

    // SELECT WORK PLACE

    const flowerShop = document.querySelector("#select-flower");
    const burgerPlace = document.querySelector("#select-burger");
    const exchange = document.querySelector("#select-exchange");
    const selectedJob = document.querySelector("#selected");
    flowerShop.addEventListener("click", function (event) {
      selectedJob.innerHTML =
        "You decided to go and wrap some flowers! Here is some cash to keep you going!";
      money.textContent = +money.textContent + 175;
    });

    burgerPlace.addEventListener("click", function (event) {
      selectedJob.innerHTML =
        "You decided to work at the Burger Shack! Have some money!";
      money.textContent = +money.textContent + 175;
    });

    exchange.addEventListener("click", function (event) {
      selectedJob.innerHTML =
        "We will trust that you count the bills correctly! Take some money!";
      money.textContent = +money.textContent + 175;
    });
  }
});
