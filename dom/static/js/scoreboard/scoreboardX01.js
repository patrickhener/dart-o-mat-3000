//Imports
import { playSound, highlightActivePlayer } from '../helper/helper.js';

// Socket IO Settings and events
let socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', () => {
  console.log('Websocket connected!');
});

socket.on('refresh', () => {
  window.location.reload(1);
});

socket.on('playSound', soundfile => {
  playSound(soundfile);
});

socket.on('redirectX01', url => {
  window.location.href = url;
});

socket.on('drawPodiumX01', (podium, word) => {
  drawPodiumX01(podium, word);
});

socket.on('drawScoreboardX01', (list, lastthrowsall, throwsum) => {
  drawScoreboardX01(list, lastthrowsall, throwsum);
});

socket.on('highlightActive', (player, round, message, average, throwcount) => {
  highlightActivePlayer(player, round, message, average, throwcount);
});

function drawScoreboardX01(list, lastthrowsall, throwsum) {
  let div = document.getElementById('score');

  while (div.firstChild) {
    div.removeChild(div.firstChild);
  }

  list.map(item => {
    let borderDiv = document.createElement('div');
    borderDiv.setAttribute('class', 'col');
    borderDiv.setAttribute('id', 'Border-' + list[item].Player);
    let nameDiv = document.createElement('div');
    nameDiv.setAttribute('name', 'Player-' + list[item].Player);
    nameDiv.setAttribute('id', 'playerName');
    nameDiv.innerHTML = "<h1 id='playerName'>" + list[item].Player + '</h1>';
    borderDiv.appendChild(nameDiv);
    let scoreDiv = document.createElement('div');
    scoreDiv.setAttribute('name', 'Score-' + list[item].Player);
    scoreDiv.setAttribute('id', 'playerScore');
    scoreDiv.innerHTML = "<h1 id='playerScore'>" + list[item].Score + '</h1>';
    borderDiv.appendChild(scoreDiv);
    let messageDiv = document.createElement('div');
    messageDiv.setAttribute('name', 'Message-' + list[item].Player);
    messageDiv.setAttribute('id', 'playerMessage');
    messageDiv.innerHTML = '';
    borderDiv.appendChild(messageDiv);
    let throwDiv = document.createElement('div');
    throwDiv.setAttribute('id', 'Throws-' + list[item].PlayerID);
    borderDiv.appendChild(throwDiv);
    let sumDiv = document.createElement('div');
    sumDiv.setAttribute('id', 'Sum-' + list[item].PlayerID);
    sumDiv.innerHTML = '';
    borderDiv.appendChild(sumDiv);
    div.appendChild(borderDiv);
  });

  lastthrowsall.map(item => {
    lastthrowsall[item].map(item2 => {
      let array = lastthrowsall[item][item2].split(',');
      throwDiv = document.getElementById('Throws-' + array[0]);
      let throww = document.createElement('div');
      throww.setAttribute('id', 'throw');
      let output = '';
      if (array[3] == '2') {
        output += 'D';
      } else if (array[3] == '3') {
        output += 'T';
      }
      output += array[2];
      throww.innerHTML = "<h2 id='playerThrow'>" + output + '</h2>';
      throwDiv.appendChild(throww);
    });
  });

  throwsum.map(item => {
    let array = throwsum[item].split(',');
    let div2 = document.getElementById('Sum-' + array[0]);
    while (div2.firstChild) {
      div2.removeChild(div2.firstChild);
    }
    sumDiv = document.getElementById('Sum-' + array[0]);
    let sum = document.createElement('div');
    sum.setAttribute('id', 'sum');
    sum.innerHTML = "<h2 id='playerSum'>" + array[1] + '</h2>';
    sumDiv.appendChild(sum);
  });
}

function drawPodiumX01(podium, word) {
  if (podium) {
    podium.map(item => {
      // array[0] = playerName
      // array[1] = podium place
      let array = podium[item].split(',');
      let scoreDiv = document.getElementsByName('Score-' + array[0]);
      scoreDiv[0].innerHTML =
        "<h1 id='playerScore'>" + word + ' ' + array[1] + '</h1>';
    });
  }
}
