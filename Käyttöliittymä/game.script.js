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

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 16,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// TUTORIAL MODAL

const helpModal = document.querySelector("#help-modal");
const helpButton = document.querySelector("#help-button");
const helpSpan = document.getElementsByClassName("close")[0];

helpButton.onclick = function () {
  helpModal.style.display = "block";
};

helpSpan.onclick = function () {
  helpModal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == helpModal) {
    helpModal.style.display = "none";
  }
};

const instructionModal = document.querySelector("#instruction-modal");
const instructionButton = document.querySelector("#instruction-button");
const instructionSpan = document.getElementsByClassName("close")[1];

instructionButton.onclick = function () {
  instructionModal.style.display = "block";
};

instructionSpan.onclick = function () {
  instructionModal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == instructionModal) {
    instructionModal.style.display = "none";
  }
};

const workModal = document.querySelector("#work-modal");
const workButton = document.querySelector("#work-button");
const workSpan = document.getElementsByClassName("close")[2];

workButton.onclick = function () {
  workModal.style.display = "block";
};

workSpan.onclick = function () {
  workModal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == workModal) {
    workModal.style.display = "none";
  }
};
