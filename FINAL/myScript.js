"use strict";

const usernameInput = document.querySelector("#query-user");
const passwordInput = document.querySelector("#query-pass");

const loginButton = document.querySelector(".login");
const registerButton = document.querySelector(".register");

const handleCredentials = {
  input() {
    return [usernameInput.value, passwordInput.value];
  },

  server(action, username, password) {
    return `http://127.0.0.1:5000/${action}?username=${username}&password=${password}`;
  },

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

function openAboutPop() {
  aboutPopup.classList.add("openAbout");
}

function closeAboutPop() {
  aboutPopup.classList.remove("openAbout");
}

let instrPop = document.getElementById('instructionsPop');

function openInstrPop() {
  instrPop.classList.add('openInstr');
}

function closeInstrPop() {
  instrPop.classList.remove('openInstr');
}

loginButton.addEventListener("click", (e) => {
  e.preventDefault();
  handleCredentials.login();
});
registerButton.addEventListener("click", (e) => {
  e.preventDefault();
  handleCredentials.register();
});

function checkPin() {
    // Get the PIN and username input values
    let pin = document.getElementById('query-pass').value;
    let username = document.getElementById('query-user').value;
    let text = document.getElementById("messageBox");

    // Match PIN to exactly 4 digits (no letters)
    const pinChecker = /^\d{4}$/;

    // Check if PIN and username are not empty, otherwise all gucci
    if (pin.trim() !== "" && username.trim() !== "" && pinChecker.test(pin) && !/[a-zA-Z]/.test(pin)) {
        text.innerText = "Credentials valid";
        text.style.color = "green";
        text.style.fontWeight = "900";
    } else {
        text.innerText = "Invalid credentials.";
        text.style.color = "red";
        text.style.fontWeight = "900";
    }
}


function toGame() {
  window.location.href = "index.html"
}












// TÄSTÄ ETEENPÄIN KOPIOITU SCRIPT.JS:STÄ

// Käyttäjän kirjoittama nimi ja PIN-koodi
const user_username = document.querySelector("#query-user");
const user_password = document.querySelector("#query-pass");

// Kirjautumis- ja rekisteröitymisnappulat
const login = document.querySelector(".login");
const register = document.querySelector(".register");

// Debug-tarkoituksiin
const result = document.querySelector(".result");

function update(person) {
  document.querySelector("#next-hint").innerHTML = person.hint;
}
async function getLogin() {
  try {
    const username = user_username.value;
    const password = user_password.value;

    const response = await fetch(
      `http://localhost:5000/login?username=${username}&password=${password}`
    );
    const json = await response.json();
    console.log(json);
    update(username);
    return json.name;
  } catch (error) {
    console.error("doLogin fail", error);
    return error;
  }
}

async function doLogin(event) {
  const response = await getLogin();
  if (response) {
    console.log(response);
    console.log("success");
    return response;
  } else {
    console.log("some Login error");
    return response.error;
  }
}

async function getRegister() {
  try {
    const username = user_username.value;
    const password = user_password.value;

    const response = await fetch(
      `http://localhost:5000/register?username=${username}&password=${password}`
    );
    const json = await response.json();
    console.log(json);
    return json.name;
  } catch (error) {
    console.error("doRegister fail", error);
    return error;
  }
}

async function doRegister() {
  const response = await getRegister();
  if (response) {
    console.log(response);
    console.log("success");
    update;
    return response;
  } else {
    console.log("some Register error");
    return response.error;
  }
}

//Ongelma: miten saada formien molemmat arvot syötettyä samalle reitille?
// const username = document.querySelector("form")[0].addEventListener("submit");

login.addEventListener("click", (e) => {
  e.preventDefault();
  result.textContent = user_username.value + " " + user_password.value;
  const promise = doLogin();
});

register.addEventListener("click", (e) => {
  e.preventDefault();
  result.textContent = user_username.value + " " + user_password.value;
  const promise = doRegister();
});



