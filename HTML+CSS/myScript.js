'use strict';

function hideFunction() {
  const pass = document.getElementById("query-pass");
  if (pass.type === "password") {
    pass.type = "text";
  } else {
    pass.type = "password";
  }
}

document.getElementById("query-pass").maxLength = "4";
document.getElementById("query-user").maxLength = "10";

let aboutPopup = document.getElementById("aboutPop");

function openAboutpop(){
  aboutPopup.classList.add('openAbout');
}

function closeAboutpop() {
  aboutPopup.classList.remove('openAbout');
}