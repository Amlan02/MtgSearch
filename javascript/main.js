let form = document.getElementById('searchForm');

//form handler
form.onsubmit = function cardSearch() {
  let input = document.getElementById('input').value;
  let searchQ = "https://api.scryfall.com/cards/search?q=" + input;
  let resultsContainer = document.getElementById('resultsContainer');
  let resultsC = document.getElementById('resultsContainer');
  let request = new XMLHttpRequest();

  resultsC.innerHTML = "";

  request.open('GET', searchQ, true)

  request.onload = function() {
    let answer = JSON.parse(this.response);

    if (request.status >= 200 && request.status < 400) {

      console.log(answer);

      const getNestedObject = (nestedObj, pathArr) => {
      return pathArr.reduce((obj, key) =>
          (obj && obj[key] !== 'undefined') ? obj[key] : undefined, nestedObj);
      }

      for(i=0; i<`${answer.total_cards}`; i++) {
        let cardImage = getNestedObject(answer, ['data', i, 'image_uris', 'normal']);
        console.log(cardImage);
        if(cardImage == undefined) {
          cardImage = "./images/notFound.jpg";
        }

        const cardName = getNestedObject(answer, ['data', i, 'name']);

        let cardPrice = "&euro;" + getNestedObject(answer, ['data', i, 'prices', 'eur']) + ",-";
        if(cardPrice == "&euro;null,-") {
          cardPrice = 'Price not found';
        }
        const gridItem = 'gridItem' + i;
          resultsC.innerHTML += `<div class='Item' id='${gridItem}'>
                                <img class='resultImage' src="${cardImage}">
                                <div class='SresultI'>
                                  <div class='info'>
                                    <p class='text'>
                                      ${cardName}<br>
                                      ${cardPrice}
                                    </p>
                                    <button class='add' onclick='add("${cardName}")'>+</button>
                                  </div>
                                </div>
                              </div>`;
      };
    } else {
        console.error(request.statusText);
    }
  }

  request.send();
  return false;
}

//buttons ClickHandler
let decklistdiv = document.getElementById('decklist');
let decklist = [];

function add(c) {
 console.log(c);
 decklist.push(c);
 writeDecklist();
}

function writeDecklist() {
  for(i=0; i<decklist.length; i++) {
    decklist.innerHTML += `<div class='deckListCard'>decklist[i]<div>`;
  }
}
