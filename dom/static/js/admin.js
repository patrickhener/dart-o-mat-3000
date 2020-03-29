var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
  console.log('Websocket connected!');
});

socket.on('redirectAdmin', function(url) {
  window.location.href = url;
});

function submitGame() {
  var playerlist = $('#player').val();
  var gametype = document.getElementById('gametype').value;
  var variant = document.getElementById('x01variant').value;
  var start = document.getElementById('startIn').value;
  var exit = document.getElementById('exitOut').value;
  var cut = document.getElementById('variant').value;
  var atcvariant = document.getElementById('atc-variant').value;
  var splitvariant = document.getElementById('split-variant').value;

  switch (gametype) {
    case 'x01':
      createX01(playerlist, variant, start, exit);
      break;
    case 'cricket':
      createCricket(playerlist, cut);
      break;
    case 'aroundtheclock':
      createATW(playerlist, atcvariant);
      break;
    case 'splitscore':
      createSplit(playerlist, splitvariant);
      break;
    default:
      alert('Something went wrong');
      break;
  }
}

function createX01(playerlist, variant, start, exit) {
  console.log('Creating X01 game...');
  socket.emit('startX01', {
    players: playerlist,
    x01variant: variant,
    startIn: start,
    exitOut: exit
  });
}

function createCricket(playerlist, cut) {
  console.log('Creating cricket game...');
  socket.emit('startCricket', { players: playerlist, variant: cut });
}

function createATW(playerlist, atcvariant) {
  console.log('Creating Around The Clock game...');
  socket.emit('startATC', { players: playerlist, variant: atcvariant });
}

function createSplit(playerlist, splitvariant) {
  console.log('Creating Split Score game...');
  socket.emit('startSplit', { players: playerlist, variant: splitvariant });
}

function hideshow() {
  var s1 = document.getElementById('gametype');
  var s2 = document.getElementById('div-x01variant');
  var s3 = document.getElementById('div-startIn');
  var s4 = document.getElementById('div-exitOut');
  var s5 = document.getElementById('div-variant');
  var s6 = document.getElementById('div-atc-variant');
  var s7 = document.getElementById('x01-rules');
  var s8 = document.getElementById('cricket-rules');
  var s9 = document.getElementById('atc-rules');
  var s10 = document.getElementById('div-splitscore-variant');
  var s11 = document.getElementById('split-rules');

  if (s1.options[s1.selectedIndex].text == 'X01') {
    s2.style.display = 'block';
    s3.style.display = 'block';
    s4.style.display = 'block';
    s5.style.display = 'none';
    s6.style.display = 'none';
    s7.style.display = 'block';
    s8.style.display = 'none';
    s9.style.display = 'none';
    s10.style.display = 'none';
    s11.style.display = 'none';
  }

  if (s1.options[s1.selectedIndex].text == 'Cricket') {
    s2.style.display = 'none';
    s3.style.display = 'none';
    s4.style.display = 'none';
    s5.style.display = 'block';
    s6.style.display = 'none';
    s7.style.display = 'none';
    s8.style.display = 'block';
    s9.style.display = 'none';
    s10.style.display = 'none';
    s11.style.display = 'none';
  }

  if (s1.options[s1.selectedIndex].text == 'Around the Clock') {
    s2.style.display = 'none';
    s3.style.display = 'none';
    s4.style.display = 'none';
    s5.style.display = 'none';
    s6.style.display = 'block';
    s7.style.display = 'none';
    s8.style.display = 'none';
    s9.style.display = 'block';
    s10.style.display = 'none';
    s11.style.display = 'none';
  }

  if (s1.options[s1.selectedIndex].text == 'Split-Score') {
    s2.style.display = 'none';
    s3.style.display = 'none';
    s4.style.display = 'none';
    s5.style.display = 'none';
    s6.style.display = 'none';
    s7.style.display = 'none';
    s8.style.display = 'none';
    s9.style.display = 'none';
    s10.style.display = 'block';
    s11.style.display = 'block';
  }
}

function hide() {
  var s1 = document.getElementById('gametype');
  var s2 = document.getElementById('div-x01variant');
  var s3 = document.getElementById('div-startIn');
  var s4 = document.getElementById('div-exitOut');
  var s5 = document.getElementById('div-variant');
  var s6 = document.getElementById('div-atc-variant');
  var s7 = document.getElementById('x01-rules');
  var s8 = document.getElementById('cricket-rules');
  var s9 = document.getElementById('atc-rules');
  var s10 = document.getElementById('div-splitscore-variant');
  var s11 = document.getElementById('split-rules');

  s1.style.display = 'block';
  s2.style.display = 'block';
  s3.style.display = 'block';
  s4.style.display = 'block';
  s5.style.display = 'none';
  s6.style.display = 'none';
  s7.style.display = 'block';
  s8.style.display = 'none';
  s9.style.display = 'none';
  s10.style.display = 'none';
  s11.style.display = 'none';
}
