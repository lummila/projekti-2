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
      // process caught an error and returns a false, console logs the error
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
      // operation caught an error, returns false and console logs the error
      console.error("Registration failed", error);
      return false;
    }
  },
};

function hideFunction() {  // hides the password from the user and shows it when checkbox is clicked
  const pass = document.getElementById("query-pass");
  if (pass.type === "password") {
    pass.type = "text";
  } else {
    pass.type = "password";
  }
}

let aboutPopup = document.getElementById("aboutPop");

function openAboutPop() { // opens a pop up with a class that turns it visible
  aboutPopup.classList.add("openAbout");
}

function closeAboutPop() {  // removes the previous class and uses the standard hidden visibility
  aboutPopup.classList.remove("openAbout");
}

let instrPop = document.getElementById("instructionsPop");

function openInstrPop() {  // opens a pop-up with a class that turns the pop up visible
  instrPop.classList.add("openInstr");
}

function closeInstrPop() { // removes the previous class, so the pop up uses the standard hidden visibility
  instrPop.classList.remove("openInstr");
}

function checkPin() {
  // Get the PIN and username input values
  const pin = passwordInput.value;
  const username = usernameInput.value;

  // Match PIN to exactly 4 digits (no letters) with a Regular Expression
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

function displayErrorMessage(message) {  // function used to present error messages in the html
  const messageBox = document.getElementById("messageBox");
  messageBox.innerText = message;
  messageBox.style.color = "red";
  messageBox.style.fontWeight = "900";
}

async function loginToGame() {
  const pinIsValid = checkPin();

  console.log(pinIsValid);
  if (pinIsValid) {  // if the PIN is valid, proceed to try to log the user in
    const loginSuccess = await handleCredentials.login();

    if (loginSuccess) {  // changes HTML to the main game if login-method returns 'true'
      window.location.href = getGameURL();
    } else { // user entered wrong password etc.
      displayErrorMessage("Check credentials");
    }
  } else {  // the pinCheck returned false
    displayErrorMessage("Invalid credentials");
  }
}

function getGameURL() {  // function to change the html file to the main game
  return "game/index.html";
}

async function registerAccount() {
  const pinIsValid = checkPin();

  if (pinIsValid) { // if the pin is valid, proceed to try to register the user
    const registrationSuccess = await handleCredentials.register();

    if (registrationSuccess) {  // changes HTML to the main game if register-method returns 'true'
      displaySuccessMessage("Account created");
      window.location.href = getGameURL();
    } else {  // else notify the player of the username being taken
      displayErrorMessage("Username taken");
    }
  } else {  // user entered invalid credentials and the checkPin returned 'false'
    displayErrorMessage("Check credentials");
  }
}

function displaySuccessMessage(message) {  // displays a message of successful registration
  displayMessage(message, "green");
}

function displayErrorMessage(message) {
  displayMessage(message, "red");
}

function displayMessage(message, color) {  // displays message in html about login instances
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
