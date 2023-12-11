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
      console.log(username, password)

      const response = await fetch(this.server("login", username, password));

      const response_json = await response.json();
      console.log(response_json)

      if (response.ok) {
        // Assuming the server returns a JSON object with a 'statusCode' property
        if (response_json.statusCode === 200) {
          // Login successful
          return true;
        } else {
          // Login failed, server returned a non-200 status code
          console.error("Login failed:", response_json.statusCode);
          return false;
        }
      } else {
        // Non-successful HTTP status code
        console.error("Login failed:", response.status);
        return false;
      }
    } catch (error) {
      console.error("Login failed", error);
      return false;
    }
  },

  async register() {
    try {
      const [username, password] = this.input();

      const response = await fetch(this.server("register", username, password));

      const response_json = await response.json();
      console.log(response_json);

      if (response.ok) {
        // Assuming the server returns a JSON object with a 'statusCode' property
        if (responseJson.statusCode === 200) {
          // Registration successful
          return true;
        } else {
          // Registration failed, server returned a non-200 status code
          console.error("Registration failed with status code:",
              responseJson.statusCode);
          return false;
        }
      } else {
        // Non-success HTTP status code
        console.error("Registration failed with status code:", response.status);
        return false;
      }
    } catch (error) {
      console.error("Registration failed", error);
      return false;
    }
  }
}

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
  const pin = document.getElementById('query-pass').value;
  const username = document.getElementById('query-user').value;

  // Match PIN to exactly 4 digits (no letters)
  const pinRegex = /^\d{4}$/;

  // Check if PIN and username are not empty, otherwise return false
  if (pin.trim() === "" || username.trim() === "") {
    displayErrorMessage("Invalid input");
    return false;
  }
  // Check if PIN is exactly 4 digits with no letters
  if (!pinRegex.test(pin) || /[a-zA-Z]/.test(pin)) {
    displayErrorMessage("Invalid PIN format");
    return false;
  }
  return true;
}




function displayErrorMessage(message) {
  const messageBox = document.getElementById("messageBox");
  messageBox.innerText = message;
  messageBox.style.color = "red";
  messageBox.style.fontWeight = "900";
}

function loginToGame() {
  const messageBox = document.getElementById("messageBox");
  const pinIsValid = checkPin();

  if (pinIsValid) {
    const loginSuccess = handleCredentials.login();

    if (loginSuccess) {
      //window.location.href = getGameURL();
    } else {
      displayErrorMessage1("Check credentials");
    }
  } else {
    displayErrorMessage1("Invalid credentials");
  }
}

function displayErrorMessage1(message) {
  const messageBox = document.getElementById("messageBox");
  messageBox.innerHTML = message;
  messageBox.style.color = "red";
  messageBox.style.fontWeight = "900";
}

function getGameURL() {
  return "game/index.html";
}


function registerAccount() {
  const messageBox = document.getElementById("messageBox");
  const pinIsValid = checkPin();

  if (pinIsValid) {
    const registrationSuccess = handleCredentials.register();

    if (registrationSuccess) {
      displaySuccessMessage("Account created");
    } else {
      displayErrorMessage2("Username taken");
    }
  } else {
    displayErrorMessage2("Check credentials");
  }
}

function displaySuccessMessage(message) {
  displayMessage(message, "green");
}

function displayErrorMessage2(message) {
  displayMessage(message, "red");
}

function displayMessage(message, color) {
  const messageBox = document.getElementById("messageBox");
  messageBox.innerText = message;
  messageBox.style.color = color;
  messageBox.style.fontWeight = "900";
}








/*
-----------------------------------------------------------------------------------
--------------------- TÄSTÄ ETEENPÄIN KOPIOITU SCRIPT.JS:STÄ-----------------------
-----------------------------------------------------------------------------------
*/



// Käyttäjän kirjoittama nimi ja PIN-koodi
const user_username = document.querySelector("#query-user");
const user_password = document.querySelector("#query-pass");

// Kirjautumis- ja rekisteröitymisnappulat
const login = document.querySelector(".login");
const register = document.querySelector(".register");

// Debug-tarkoituksiin
//  const result = document.querySelector(".result");


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
/*
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
*/


