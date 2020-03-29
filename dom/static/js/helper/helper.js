function playSound(soundfile) {
  if (soundfile != null) {
    var audio = new Audio(
      'http://' +
        document.domain +
        ':' +
        location.port +
        '/static/sounds/' +
        soundfile +
        '.mp3'
    );
    audio.play();
  }
}

function highlightActivePlayer(
  activePlayer,
  playerRound,
  message,
  average,
  throwcount
) {
  var borderDiv = document.getElementById('Border-' + activePlayer);
  borderDiv.style.border = '5px solid white';
  borderDiv.style.boxShadow = '10px 10px 15px black';
  var divActivePlayer = document.getElementById('header-activePlayer');
  divActivePlayer.innerHTML = activePlayer;
  var divRndcount = document.getElementById('header-rndcount');
  divRndcount.innerHTML = playerRound;
  var divAverage = document.getElementById('header-average');
  divAverage.innerHTML = average;
  var divThrowcount = document.getElementById('header-throwcount');
  divThrowcount.innerHTML = throwcount;
  var messageDiv = document.getElementsByName('Message-' + activePlayer);
  messageDiv[0].innerHTML = '<h1>' + message + '</h1>';
}

export { playSound, highlightActivePlayer };
