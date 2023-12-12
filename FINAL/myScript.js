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
      console.log(username, password);

      const response = await fetch(
        this.server("login", username.toUpperCase(), password)
      );

      const response_json = await response.json();
      console.log(response_json);

      if (response.ok) {
        // Assuming the server returns a JSON object with a 'statusCode' property
        if (response.ok) {
          // Login successful
          return true;
        } else {
          // Login failed, server returned a non-200 status code
          console.error("Login failed:", response.status);
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

      if (!Object.keys(response_json).includes("ERROR")) {
        // Registration successful
        return true;
      } else {
        // Non-success HTTP status code
        console.error("Registration failed:", response.error);
        return false;
      }
    } catch (error) {
      console.error("Registration failed", error);
      return false;
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

let aboutPopup = document.getElementById("aboutPop");

function openAboutPop() {
  aboutPopup.classList.add("openAbout");
}

function closeAboutPop() {
  aboutPopup.classList.remove("openAbout");
}

let instrPop = document.getElementById("instructionsPop");

function openInstrPop() {
  instrPop.classList.add("openInstr");
}

function closeInstrPop() {
  instrPop.classList.remove("openInstr");
}

function checkPin() {
  // Get the PIN and username input values
  const pin = passwordInput.value;
  const username = usernameInput.value;

  // Match PIN to exactly 4 digits (no letters)
  const pinRegex = /\D/g;

  // Check if PIN and username are not empty, otherwise return false
  if (pin.trim() === "" || username.trim() === "") {
    displayErrorMessage("Invalid input");
    return false;
  }
  // Check if PIN is exactly 4 digits with no letters
  if (pin.length !== 4 || pinRegex.test(pin) || /[a-zA-Z]/.test(pin)) {
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

async function loginToGame() {
  const pinIsValid = checkPin();

  console.log(pinIsValid);
  if (pinIsValid) {
    const loginSuccess = await handleCredentials.login();

    if (loginSuccess) {
      window.location.href = getGameURL();
    } else {
      displayErrorMessage("Check credentials");
    }
  } else {
    displayErrorMessage("Invalid credentials");
  }
}

function getGameURL() {
  return "game/index.html";
}

async function registerAccount() {
  const pinIsValid = checkPin();

  if (pinIsValid) {
    const registrationSuccess = await handleCredentials.register();

    if (registrationSuccess) {
      displaySuccessMessage("Account created");
      window.location.href = getGameURL();
    } else {
      displayErrorMessage("Username taken");
    }
  } else {
    displayErrorMessage("Check credentials");
  }
}

function displaySuccessMessage(message) {
  displayMessage(message, "green");
}

function displayErrorMessage(message) {
  displayMessage(message, "red");
}

function displayMessage(message, color) {
  const messageBox = document.getElementById("messageBox");
  messageBox.innerText = message;
  messageBox.style.color = color;
  messageBox.style.fontWeight = "900";
}

loginButton.addEventListener("click", (e) => {
  e.preventDefault();
  loginToGame();
});
registerButton.addEventListener("click", (e) => {
  e.preventDefault();
  registerAccount();
});
