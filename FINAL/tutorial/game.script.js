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
  async update() {
    const data = await this.fetchInfo();
    // HUOM VAIN KEHITYSTARPEISIIN
    console.log(data);

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
    }).addTo(map);
    marker.bindPopup(data.location.airport_name);
    //Käydään läpi kaikki mahdollisten kohteiden koordinaatit ja laitetaan pisteet niiden päälle
    console.log(airports);
    for (const i in airports) {
      console.log(airports[i].coordinates);
      const dot = L.marker(airports[i].coordinates, {
        title: airports[i].airport_name,
      }).addTo(map);
      dot.bindPopup(airports[i].airport_name);
    }
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

tutorial.textContent =
  "Welcome to the tutorial! In this short interactive demonstration, you will learn to play Velkajahti. We will go over flying to different countries and working for money. Press the 'Work' button to continue.";

workButton.addEventListener;
"click",
  () => {
    let pressed = false;

    return () => {
      if (!pressed) {
        !pressed;
      }
    };
  };

/*
const workModal = document.querySelector("#work-modal");
const workButton = document.querySelector("#work-button");
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
});

burgerPlace.addEventListener("click", function (event) {
  selectedJob.innerHTML =
    "You decided to work at the Burger Shack! Have some money!";
});

exchange.addEventListener("click", function (event) {
  selectedJob.innerHTML =
    "We will trust that you count the bills correctly! Take some money!";
});
*/
