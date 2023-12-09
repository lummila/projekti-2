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

let aboutPopup = document.getElementById("aboutPop");

function openAboutpop() {
  aboutPopup.classList.add("openAbout");
}

function closeAboutpop() {
  aboutPopup.classList.remove("openAbout");
}

let instrPop = document.getElementById("instructionsPop");

function openInstrPop() {
  instrPop.classList.add("openInstr");
}

function closeInstrPop() {
  instrPop.classList.remove("openInstr");
}

loginButton.addEventListener("click", (e) => {
  e.preventDefault();
  handleCredentials.login();
});
registerButton.addEventListener("click", (e) => {
  e.preventDefault();
  handleCredentials.register();
});
