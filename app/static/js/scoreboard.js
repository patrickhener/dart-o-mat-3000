var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
     console.log('Websocket connected!');
});

socket.on('refresh', function() {
	window.location.reload(1);
});

socket.on('drawScoreboardX01', function(list, lastthrowsall, throwsum) {
	console.log(throwsum);
	drawScoreboardX01(list, lastthrowsall, throwsum);
});

socket.on('highlightActive', function(player, playerID, round, message, average, throwcount) {
	highlightActivePlayer(player, playerID, round, message, average, throwcount);
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
function drawScoreboardX01(list, lastthrowsall, throwsum) {
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
	for (var item in lastthrowsall) {
		var array = lastthrowsall[item].split(",");
		var throwDiv = document.getElementById("Throws-" + array[0]);
		var throww = document.createElement("div");
		throww.setAttribute("id", "throw");
		throww.innerHTML = "<h2 id='playerThrow'>" + array[1] + "</h2>";
		throwDiv.appendChild(throww);
	}

	for (var item in throwsum) {
		var array = throwsum[item].split(",");
		var div2 = document.getElementById("Sum-" + array[0]);
		while(div2.firstChild) {
			div2.removeChild(div2.firstChild);
		}
		var sumDiv = document.getElementById("Sum-" + array[0]);
		var sum = document.createElement("div");
		sum.setAttribute("id", "sum");
		sum.innerHTML = "<h2 id='playerSum'>" + array[1] + "</h2>";
		sumDiv.appendChild(sum);
	}
};

function highlightActivePlayer(activePlayer, playerID, playerRound, message, average, throwcount) {
	var borderDiv = document.getElementById("Border-" + activePlayer);
	borderDiv.style.border='5px solid white';
	borderDiv.style.boxShadow='10px 10px 15px black';
	var headerLeft = document.getElementById("header-left");
	headerLeft.innerHTML = "<b>Active Player: " + activePlayer + "<br>Player round: " + playerRound + "<br>Player Average: " + average + "<br>Player Throws: " + throwcount + "</b>";
	var messageDiv = document.getElementsByName("Message-" + activePlayer);
	messageDiv[0].innerHTML = message;
	var throwDiv = document.getElementById("Throws-" + playerID);
};
