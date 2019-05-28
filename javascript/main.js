function cardSearch() {
  let input = document.getElementById('input').value;
  let searchQ = "https://api.scryfall.com/cards/search?q=" + input;
  let resultsContainer = document.getElementById('resultsContainer');
  let textbox = document.getElementById('textbox');
  let request = new XMLHttpRequest();

  request.open('GET', searchQ, true)

  request.timeout = 500;

  request.onload = function() {
    let answer = JSON.parse(this.response);

    if (request.status >= 200 && request.status < 400) {

      console.log(answer);

      const getNestedObject = (nestedObj, pathArr) => {
      return pathArr.reduce((obj, key) =>
          (obj && obj[key] !== 'undefined') ? obj[key] : undefined, nestedObj);
      }

      const cardImage = getNestedObject(answer, ['data', 0, 'image_uris', 'normal']);

      textbox.innerHTML = `Found ${answer.total_cards} cards.<br>
                           First result: ${answer.data[0].name}<br>
                           <img id='resultImage' src="${cardImage}">`;

    } else {
        console.log('error');
    }
  }

  request.send()

  return false;
}
