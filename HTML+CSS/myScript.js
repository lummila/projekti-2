"use strict";

// Käyttäjän kirjoittama nimi ja PIN-koodi
const usernameInput = document.querySelector("#query-user");
const passwordInput = document.querySelector("#query-pass");

// Kirjautumis- ja rekisteröitymisnappulat
const loginButton = document.querySelector(".login");
const registerButton = document.querySelector(".register");

const handleCredentials = {
  // Lyhyt funktio, joka palauttaa tekstikenttien arvot eli kirjatut tekstit
  input() {
    return [usernameInput.value, passwordInput.value];
  },
  // fetch-osoite, action on joko login tai register, ja muut tulevat käyttäjän tekstistä
  server(action, username, password) {
    return `http://127.0.0.1:5000/${action}?username=${username}&password=${password}`;
  },
  // Kirjautumisfunktio, joka palauttaa pelaajan tiedot
  async login() {
    try {
      const [username, password] = this.input();

      const response = await fetch(this.server("login", username, password));

      const response_json = await response.json();
      console.log(response_json);

      return response_json;
    } catch (error) {
      console.error("Login failed", error);
      return error;
    }
  },
  // Sama kuin ylempi, mutta rekisteröityminen
  async register() {
    try {
      const [username, password] = this.input();

      const response = await fetch(this.server("register", username, password));

      const response_json = await response.json();
      console.log(response_json);

      return response_json;
    } catch (error) {
      console.error("Registering failed", error);
      return error;
    }
  },
};

// EventListenerit kirjautumiselle ja rekisteröitymiselle.
// preventDefault estää HTML-osoitteen muuttumisen, JS käsittelee pyynnön
loginButton.addEventListener("click", (e) => {
  e.preventDefault();
  handleCredentials.login();
});
registerButton.addEventListener("click", (e) => {
  e.preventDefault();
  handleCredentials.register();
});

function hideFunction() {
  const pass = document.getElementById("query-pass");
  if (pass.type === "password") {
    pass.type = "text";
  } else {
    pass.type = "password";
  }
}

// document.getElementById("query-pass").maxLength = "4";
// document.getElementById("query-user").maxLength = "10";

let aboutPopup = document.getElementById("aboutPop");

function openAboutpop() {
  aboutPopup.classList.add("openAbout");
}

function closeAboutpop() {
  aboutPopup.classList.remove("openAbout");
}
