let form = document.getElementById('searchForm');

form.onsubmit = function cardSearch() {
  let input = document.getElementById('input').value;
  let searchQ = "https://api.scryfall.com/cards/search?q=" + input;
  let resultsContainer = document.getElementById('resultsContainer');
  let textbox = document.getElementById('textbox');
  let request = new XMLHttpRequest();

  textbox.innerHTML = "";

  request.open('GET', searchQ, true)

  request.onload = function() {
    let answer = JSON.parse(this.response);

    if (request.status >= 200 && request.status < 400) {

      console.log(answer);

      const getNestedObject = (nestedObj, pathArr) => {
      return pathArr.reduce((obj, key) =>
          (obj && obj[key] !== 'undefined') ? obj[key] : undefined, nestedObj);
      }

    //  const cardImage = getNestedObject(answer, ['data', 0, 'image_uris', 'normal']);

      for(i=0; i<`${answer.total_cards}`; i++) {
        const cardImage = getNestedObject(answer, ['data', i, 'image_uris', 'normal']);
        textbox.innerHTML += `<img class='resultImage' src="${cardImage}">`;
      }

      // textbox.innerHTML = `Found ${answer.total_cards} cards.<br>
      //                      First result: ${answer.data[0].name}<br>
      //                      <img id='resultImage' src="${cardImage}">`;

    } else {
        console.error(request.statusText);
    }
  }

  request.send()

  return false;
}
