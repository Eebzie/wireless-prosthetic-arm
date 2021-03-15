const header = document.querySelector('header');
const section = document.querySelector('section');

let requestURL = 'https://raw.githubusercontent.com/Eebzie/wireless-prosthetic-arm/main/data.json';
let request = new XMLHttpRequest();
request.open('GET', requestURL);
request.responseType = 'json';
request.send();

request.onload = function() {
    const superHeroes = request.response;
//   populateHeader(superHeroes);
    showHeroes(superHeroes);
}

// function populateHeader(obj) {
//   const myH1 = document.createElement('h1');
//   myH1.textContent = obj['squadName'];
//   header.appendChild(myH1);

//   const myPara = document.createElement('p');
//   myPara.textContent = 'Hometown: ' + obj['homeTown'] + ' // Formed: ' + obj['formed'];
//   header.appendChild(myPara);
// }

function showHeroes(obj) {
    const heroes = obj['sensors'];

    for(let i = 0; i < heroes.length; i++) {
    // const myArticle = document.createElement('article');
    // const myH2 = document.createElement('h2');
    // const myPara1 = document.createElement('p');
    // const myPara2 = document.createElement('p');
    // const myPara3 = document.createElement('p');
    // const myList = document.createElement('ul');

    // myH2.textContent = heroes[i].sn;
    // // myPara1.textContent = 'Secret identity: ' + heroes[i].secretIdentity;
    // myPara2.textContent = 'Finger Temperature Sensor: ' + heroes[i].fingSens + '*C';
    // // myPara3.textContent = 'Superpowers:';

    // // const superPowers = heroes[i].powers;
    // // for(let j = 0; j < superPowers.length; j++) {
    // //   const listItem = document.createElement('li');
    // //   listItem.textContent = superPowers[j];
    // //   myList.appendChild(listItem);
    // // }

    // myArticle.appendChild(myH2);
    // myArticle.appendChild(myPara1);
    // myArticle.appendChild(myPara2);
    // myArticle.appendChild(myPara3);
    // myArticle.appendChild(myList);
    // section.appendChild(myArticle);

    document.getElementById("fingerTemp").innerHTML=heroes[i].fingSens+'°C';
    document.getElementById("internalTemp").innerHTML=heroes[i].intSens+'°C';
    }
}