"use strict";

// Pelaajan vinkki seuraavaan kohteeseen
const hint = document.querySelector("#next-hint");

// Elementtilista kaikista lentokenttänappuloista
const icaoButtons = document.querySelectorAll(".icao-button");

// Pelaajan viimeisin sattuma
const coincidence = document.querySelector("#given-coincidence");

// Pelaajan raha-, päästö- ja kierrostilanteet
const money = document.querySelector("#money");
const emissions = document.querySelector("#emissions");
const round = document.querySelector("#round");

// PELILOGIIKAN KÄSITTELY
const gameLogic = {
  async fetchInfo() {
    try {
      //
      const response = await fetch("http://127.0.0.1:5000/update?fly=no");
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
    // Vinkkiteksti
    hint.textContent = data.hint;

    // Otetaan tuodusta datasta vain lentokentät-osio
    const airports = data.possible_destinations;
    // Käydään jokainen ICAO-nappula läpi ja sijoitetaan niihin oikeat tiedot
    icaoButtons.forEach((e, i) => {
      // Otetaan ylös tämänhetkisen iteraation ICAO-koodi
      const icao = Object.keys(airports)[i];
      // e on ICAO-nappula ja siihen syötetään teksti airports-objektista icao-koodin avulla
      e.textContent = `${airports[icao].airport_name}, ${airports[icao].country_name}`;
    });
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

const map = L.map("map").setView([60.31, 24.94], 13);
const mapElement = document.querySelector("#map");

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 16,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// MODALS

const personalModal = document.querySelector("#personal-modal");
const personalButton = document.querySelector("#personal-button");
const personalSpan = document.getElementsByClassName("close")[0];

personalButton.onclick = function () {
  // Piilotetaan kartta
  mapElement.classList.add("hidden");
  personalModal.style.display = "block";
};

personalSpan.onclick = function () {
  // Näytetään kartta taas
  mapElement.classList.remove("hidden");
  personalModal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == personalModal) {
    personalModal.style.display = "none";
  }
};

const leaderModal = document.querySelector("#leader-modal");
const leaderButton = document.querySelector("#leader-button");
const leaderSpan = document.getElementsByClassName("close")[1];

leaderButton.onclick = function () {
  // Piilotetaan kartta
  mapElement.classList.add("hidden");
  leaderModal.style.display = "block";
};

leaderSpan.onclick = function () {
  // Näytetään kartta taas
  mapElement.classList.remove("hidden");
  leaderModal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == leaderModal) {
    leaderModal.style.display = "none";
  }
};

const helpModal = document.querySelector("#help-modal");
const helpButton = document.querySelector("#help-button");
const helpSpan = document.getElementsByClassName("close")[3];

helpButton.onclick = function () {
  // Piilotetaan kartta
  mapElement.classList.add("hidden");
  helpModal.style.display = "block";
};

helpSpan.onclick = function () {
  // Näytetään kartta taas
  mapElement.classList.remove("hidden");
  helpModal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == helpModal) {
    helpModal.style.display = "none";
  }
};

const instructionModal = document.querySelector("#instruction-modal");
const instructionButton = document.querySelector("#instruction-button");
const instructionSpan = document.getElementsByClassName("close")[2];

instructionButton.onclick = function () {
  // Piilotetaan kartta
  mapElement.classList.add("hidden");
  instructionModal.style.display = "block";
};

instructionSpan.onclick = function () {
  // Näytetään kartta taas
  mapElement.classList.remove("hidden");
  instructionModal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == instructionModal) {
    instructionModal.style.display = "none";
  }
};

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
