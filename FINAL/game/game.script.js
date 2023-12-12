"use strict";

// TÄRKEÄ: PELAAJAN TIEDOT OVAT LOKAALISTI TALLENNETTU TÄHÄN!
let playerData = {};
// Jos playerData.final_score on olemassa, peli päättyy
// Kaikkien pisteille
let leaderboard = {};
// Omille pisteille
let personal_leaderboard = {};

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

// Henkilökohtaiset parhaat pisteet
const personalModal = document.querySelector("#personal-modal");
const personalButton = document.querySelector("#personal-button");
const personalSpan = document.getElementsByClassName("close")[0];

const personalScores = document.querySelectorAll(".score");

// Parhaiden pisteiden lista
const leaderModal = document.querySelector("#leader-modal");
const leaderButton = document.querySelector("#leader-button");
const leaderSpan = document.getElementsByClassName("close")[1];

const leaderboardNames = document.querySelectorAll(".user-name");
const leaderboardScores = document.querySelectorAll(".top-score");

// Instructions-nappula
const instructionModal = document.querySelector("#instruction-modal");
const instructionButton = document.querySelector("#instruction-button");
const instructionSpan = document.getElementsByClassName("close")[2];

// Help-nappulan elementit
const helpModal = document.querySelector("#help-modal");
const helpButton = document.querySelector("#help-button");
const helpSpan = document.getElementsByClassName("close")[3];

// EXIT-nappula
const exitModal = document.querySelector("#exit-modal");
const exitButton = document.querySelector("#exit-button");
const exitSpan = document.getElementsByClassName("close")[4];

// Work-nappula
const workModal = document.querySelector("#work-modal");
const workButton = document.querySelector("#work-button");
const workSpan = document.getElementsByClassName("close")[5];

const jobElement = document.querySelector(".selected-job");
jobElement.classList.add("hidden");

// Kartan elementti ja täppien listan luominen
const map = L.map("map").setView([60.31, 24.94], 4);
const mapElement = document.querySelector("#map");
const markers = L.layerGroup();

// Työpaikat ja työskentely
const flowerShop = document.querySelector("#select-flower");
const burgerPlace = document.querySelector("#select-burger");
const exchange = document.querySelector("#select-exchange");
const selectedJob = document.querySelector("#selected");

const continueGame = document.querySelector(".continue");
continueGame.classList.add("hidden");

const addMoney = document.querySelector("#continue");

// Pelin voitto- ja häviämodaalit
const winnerModal = document.querySelector("#winner-modal");
const yourPoints = document.querySelector(".your-points");
const loserModal = document.querySelector(".loser-modal");

// Ikonit
const blueIcon = L.divIcon({ className: "blue-icon" });
const greenIcon = L.divIcon({ className: "green-icon" });

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 500,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// PELILOGIIKAN KÄSITTELY
const gameLogic = {
  async fetchInfo() {
    try {
      //
      const response = await fetch("http://127.0.0.1:5000/update");
      if (!response.ok) {
        console.error("Error in fetchInfo()", response.error);
      }
      const response_json = await response.json();

      playerData = await response_json;
      this.update();
    } catch (error) {
      console.error("Error updating game data", error);
      return error;
    }
  },

  async fly(destination) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/fly?dest=${destination}`
      );
      if (!response.ok) {
        console.error("fly() failed", response.error);
        return response;
      }
      const response_json = await response.json();

      playerData = response_json;
      this.update();
    } catch (error) {
      console.error("Error in fly()", error);
    }
  },

  async work() {
    try {
      const response = await fetch("http://127.0.0.1:5000/work");

      if (!response.ok) {
        console.error("Error in work()", response.error);
      }

      const response_json = await response.json();
      playerData = response_json;
      this.update();
    } catch (error) {
      console.error("Error in fetching work()", error);
    }
  },

  async highScore(personal) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/highscore?personal=${personal ? true : false}`
      );
      if (!response.ok) {
        console.error("Error in highScore(personal)", response.error);
      }

      const response_json = await response.json();

      return response_json;
    } catch (error) {
      console.error("Error in highScore()", error);
    }
  },

  update() {
    // Päivitys alkaa siitä, että otetaan lokaalisti tallennettu pelaajan tieto käyttöön
    const data = playerData;

    if (data.final_score) {
      yourPoints.textContent = `Your points: ${playerData.final_score}`;
      mapElement.classList.add("hidden");
      winnerModal.style.display = "block";
    }
    if (playerData.round >= 10) {
      mapElement.classList.add("hidden");
      loserModal.style.display = "block";
    }

    // Tyhjennetään kartta täpistä
    markers.clearLayers();
    // HUOM VAIN KEHITYSTARPEISIIN
    // console.log(data);
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
      e.onclick = () => gameLogic.fly(icao);
    });

    //for looppi joka laittaa täpät kartalle
    for (const i in airports) {
      const dot = L.marker(airports[i].coordinates);
      //väri
      dot.setIcon(greenIcon);
      dot.bindPopup(airports[i].airport_name);
      markers.addLayer(dot);
      //markerArray += airports[i].coordinates;
      //Tekee näppäimen, joka aukeaa klikkauksella
      const popupContent = document.createElement("div");
      const h4 = document.createElement("p");
      h4.innerHTML = airports[i].airport_name;
      popupContent.append(h4);
      //const flyButton = document.createElement('button');
      //flyButton.classList.add('button');
      //flyButton.innerHTML = `Fly here`;
      //popupContent.append(flyButton);
      dot.bindPopup(popupContent);
      markers.addLayer(dot);
    }
    // Karttapiste nykyiselle sijainnille
    const marker = L.marker(data.location.coordinates);
    marker.bindPopup(`You are here: ${data.location.airport_name}`);
    marker.openPopup();
    marker.setIcon(blueIcon);
    markers.addLayer(marker);
    //const group = new L.featureGroup(markerArray);
    //map.fitBounds([markerArray]);
    // Laitetaan kaikki luodut täpät esille kartalle
    map.addLayer(markers);
    // Lennättää näkymän nykyiseen sijaintiin
    const currlocation = data.location.coordinates;
    map.flyTo(currlocation, 4);
    // Sattumateksti
    coincidence.textContent = data.coincidence;
    // Rahamäärä
    money.textContent = data.money + "€";
    // Emissiomäärä
    emissions.textContent = data.emissions + "kg";
    // Kierros
    round.textContent = data.round;
    //kartta
  },
  async reset() {
    try {
      const response = await fetch("http://127.0.0.1:5000/reset");
      if (!response.ok) {
        console.error("Error fetching reset()", response.error);
      }

      const response_json = await response.json();
      playerData = response_json;

      this.update();
    } catch (error) {
      console.error("Error in resert()", error);
    }
  },
};

gameLogic.fetchInfo();

personalButton.onclick = async function () {
  personal_leaderboard = await gameLogic.highScore(true);
  console.log(personal_leaderboard);
  // Piilotetaan kartta
  mapElement.classList.add("hidden");
  personalModal.style.display = "block";

  for (let i = 0; i < Object.keys(personal_leaderboard).length; i++) {
    personalScores[i].textContent = Object.values(personal_leaderboard)[i];
  }
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

leaderButton.onclick = async function () {
  leaderboard = await gameLogic.highScore(false);
  // Piilotetaan kartta
  mapElement.classList.add("hidden");
  leaderModal.style.display = "block";

  for (let i = 0; i < Object.keys(leaderboard).length; i++) {
    const name = Object.keys(leaderboard)[i];
    const points = Object.values(leaderboard)[i];

    leaderboardNames[i].textContent = name;
    leaderboardScores[i].textContent = points;
  }
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

exitButton.onclick = function () {
  // Piilotetaan kartta
  mapElement.classList.add("hidden");
  exitModal.style.display = "block";
};

exitSpan.onclick = function () {
  // Näytetään kartta taas
  mapElement.classList.remove("hidden");
  exitModal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == exitModal) {
    exitModal.style.display = "none";
  }
};

function exitToMain() {
  window.location = "../index.html";
}

workButton.onclick = function () {
  // Piilotetaan kartta
  mapElement.classList.add("hidden");
  workModal.style.display = "block";
};

workSpan.onclick = function () {
  // Näytetään kartta taas
  mapElement.classList.remove("hidden");
  jobElement.classList.add("hidden");
  continueGame.classList.add("hidden");
  workModal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == workModal) {
    workModal.style.display = "none";
  }
};

addMoney.addEventListener("click", function (event) {
  jobElement.classList.add("hidden");
  continueGame.classList.add("hidden");
  mapElement.classList.remove("hidden");
  workModal.style.display = "none";
});

flowerShop.addEventListener("click", function (event) {
  jobElement.classList.remove("hidden");
  continueGame.classList.remove("hidden");

  gameLogic.work();

  selectedJob.innerHTML =
    "You decided to go and wrap some flowers! Here is some cash to keep you going! <br> Click CONTINUE to save and add 175€ to your account.";
});

burgerPlace.addEventListener("click", function (event) {
  jobElement.classList.remove("hidden");
  continueGame.classList.remove("hidden");

  gameLogic.work();

  selectedJob.innerHTML =
    "You decided to work at the Burger Shack! Have some money! <br> Click CONTINUE to save and add 175€ to your account.";
});

exchange.addEventListener("click", function (event) {
  jobElement.classList.remove("hidden");
  continueGame.classList.remove("hidden");

  gameLogic.work();

  selectedJob.innerHTML =
    "We will trust that you count the bills correctly! Take some money! <br> Click CONTINUE to save and add 175€ to your account.";
});
