
'use strict'


async function getLogin(username){
  try{
    const response = await fetch('http://localhost:5000/register');
    const json = response.json();
    console.log(json.name);
    return json.name;
  } catch (error){
    console.error("doLogin fail", error);
  }
}

async function doLogin(event){
  event.preventDefault();
  const username = document.getElementById('query').value;
  const response= await getLogin(username);
  const response2 = await getPassword(password);
    if (response){
      console.log(response);
      console.log("success");
      return (response)
  } else{
    console.log("some error");
    return (response.error);
  }
}
//Ongelma: miten saada formien molemmat arvot syötettyä samalle reitille?
const username = document.querySelector('form')[0].addEventListener('submit');
document.querySelector('form')[1].addEventListener('submit', doLogin);