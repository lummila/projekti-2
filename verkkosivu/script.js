"use strict";

const user_username = document.querySelector("#query-user");
const user_password = document.querySelector("#query-pass");

const login = document.querySelector(".login");
const register = document.querySelector(".register");

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

async function doRegister(event) {
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
