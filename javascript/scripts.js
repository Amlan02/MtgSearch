var request = new XMLHttpRequest();

request.open('GET', 'https://api.scryfall.com/cards/search?q=c%3Awhite+cmc%3D1', true)

request.onload = function() {

  var data = JSON.parse(this.response)

  if (request.status >= 200 && request.status < 400) {
    console.log(data);
  } else {
    console.log('error')
  }
}

request.send()
