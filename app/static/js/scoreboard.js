var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
     console.log('Websocket connected!');
});

socket.on('refresh', function() {
	window.location.reload(1);
});

socket.on('drawScoreboardX01', function(list) {
	drawScoreboardX01(list);
});

socket.on('highlightActive', function(player, round, message) {
	highlightActivePlayer(player, round, message);
});

socket.on('redirectX01', function(url) {
	window.location.href = url;
});

socket.on('redirectCricket', function(url) {
	window.location.href = url;
});

// Functions
function drawScoreboardX01(list) {
	var div = document.getElementById("score");
	while (div.firstChild) {
		div.removeChild(div.firstChild);
	}
	for (var item in list) {
		var div = document.getElementById("score");
		var borderDiv = document.createElement("div");
		borderDiv.setAttribute("class", "col");
		borderDiv.setAttribute("id", "Border-" + list[item].Player);
		var nameDiv = document.createElement("div");
		nameDiv.setAttribute("name", "Player-" + list[item].Player);
		nameDiv.setAttribute("id", "playerName");
		nameDiv.innerHTML = "<h1 id='playerName'>" + list[item].Player + "</h1>";
		borderDiv.appendChild(nameDiv);
		var scoreDiv = document.createElement("div");
		scoreDiv.setAttribute("name", "Score-" + list[item].Player);
		scoreDiv.setAttribute("id", "playerScore");
		scoreDiv.innerHTML = "<h1 id='playerScore'>" + list[item].Score + "</h1>";
		borderDiv.appendChild(scoreDiv);
		var messageDiv = document.createElement("div");
		messageDiv.setAttribute("name", "Message-" + list[item].Player);
		messageDiv.setAttribute("id", "playerMessage");
		messageDiv.innerHTML = "";
		borderDiv.appendChild(messageDiv);
		var throwDiv = document.createElement("div");
		throwDiv.setAttribute("name", "Throw-" + list[item].Player);
		throwDiv.setAttribute("id", "playerThrow");
		throwDiv.innerHTML = "";
		borderDiv.appendChild(throwDiv);
		div.appendChild(borderDiv);
	}
};

function highlightActivePlayer(activePlayer, playerRound, message) {
	var borderDiv = document.getElementById("Border-" + activePlayer);
	borderDiv.style.border='5px solid white';
	borderDiv.style.boxShadow='10px 10px 15px black';
	var headerLeft = document.getElementById("header-left");
	headerLeft.innerHTML = "<b>Active Player: " + activePlayer + "<br>Player round: " + playerRound + "<br>Player Average: </b>";
	var messageDiv = document.getElementsByName("Message-" + activePlayer);
	messageDiv[0].innerHTML = message;
};

function init(list, activePlayer) {
	drawScoreboardX01(list);
	highlightActivePlayer(activePlayer);
};
