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

socket.on('highlightActive', function(player, round, message, average) {
	highlightActivePlayer(player, round, message, average);
});

socket.on('refreshAverage', function(average) {
	refreshAverage(average);
});

socket.on('updateThrow', function(count,playerid) {
	updateThrows(count,playerid);
});

socket.on('redirectX01', function(url) {
	window.location.href = url;
});

socket.on('redirectCricket', function(url) {
	window.location.href = url;
});

// Functions
function drawScoreboardX01(list, throwcount, playerid) {
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
		throwDiv.setAttribute("id", "Throws-" + list[item].PlayerID);
		borderDiv.appendChild(throwDiv);
		var sumDiv = document.createElement("div");
		sumDiv.setAttribute("id", "Sum-" + list[item].PlayerID);
		sumDiv.innerHTML="";
		borderDiv.appendChild(sumDiv);
		div.appendChild(borderDiv);
	}
};

function highlightActivePlayer(activePlayer, playerRound, message, average) {
	var borderDiv = document.getElementById("Border-" + activePlayer);
	borderDiv.style.border='5px solid white';
	borderDiv.style.boxShadow='10px 10px 15px black';
	var headerLeft = document.getElementById("header-left");
	headerLeft.innerHTML = "<b>Active Player: " + activePlayer + "<br>Player round: " + playerRound + "<br>Player Average: " + average + "</b>";
	var messageDiv = document.getElementsByName("Message-" + activePlayer);
	messageDiv[0].innerHTML = message;
};

function updateThrows(throwcount,playerid) {
	// Well the point is this is working, when not pretty, but working
	// But because the scoreboard is redrawn every time it gets requested, so this will not be displayed permanent
	var throwsDiv = document.getElementById("Throws-" + playerid);
	if (throwsDiv.childNodes.length == 3) {
		while (throwsDiv.firstChild) {
			throwsDiv.removeChild(throwsDiv.firstChild);
		}
	}
	countDiv = document.createElement("div");
	countDiv.setAttribute("id", "playerThrow");
	countDiv.innerHTML = throwcount;
	throwsDiv.appendChild(countDiv);
};
