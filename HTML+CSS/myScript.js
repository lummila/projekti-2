'use strict';

function hideFunction() {
  const x = document.getElementById("query-pass");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

document.getElementById("query-pass").maxLength = "4";
