'use strict';

const map = L.map('map').setView([60.31, 24.94], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 16,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// TUTORIAL MODAL

const helpModal = document.querySelector('#help-modal');
const helpButton = document.querySelector('#help-button');
const helpSpan = document.getElementsByClassName('close')[0];

helpButton.onclick = function () {
    helpModal.style.display = "block";
}

helpSpan.onclick = function () {
    helpModal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == helpModal) {
        helpModal.style.display = "none";
    }
}

const instructionModal = document.querySelector('#instruction-modal');
const instructionButton = document.querySelector('#instruction-button');
const instructionSpan = document.getElementsByClassName('close')[1];

instructionButton.onclick = function () {
    instructionModal.style.display = "block";
}

instructionSpan.onclick = function () {
    instructionModal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == instructionModal) {
        instructionModal.style.display = "none";
    }
}

const workModal = document.querySelector('#work-modal');
const workButton = document.querySelector('#work-button');
const workSpan = document.getElementsByClassName('close')[2];

workButton.onclick = function () {
    workModal.style.display = "block";
}

workSpan.onclick = function () {
    workModal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == workModal) {
        workModal.style.display = "none";
    }
}
