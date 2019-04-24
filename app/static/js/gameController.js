var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
});

socket.on('redirectGameController', function(url) {
	window.location.href = url;
});

socket.on('drawX01Controller', function() {
	drawX01Controller();
});

socket.on('drawCricketController', function() {
	drawCricketController();
});

socket.on('drawThrows', function(playerlist, throwlist) {
	drawThrows(playerlist, throwlist);
});

socket.on('rematchButton', function() {
	rematchButton();
});

socket.on('highlightAndScore', function(activePlayer, scorelist) {
	highlightAndScore(activePlayer, scorelist);
});

socket.on('highlightCricket', function(activePlayer) {
	highlightAndScore(activePlayer);
});

socket.on('drawATC', function (number) {
	drawATC(number);
});

socket.on('highlightATC', function (activePlayer) {
	highlightATC(activePlayer);
});

function drawX01Controller() {
	var div = document.getElementById("controls");
	while (div.firstChild) {
		div.removeChild(div.firstChild);
	}
	var borderDiv = document.getElementById("controls");
	var groupDiv = document.createElement("div");
	groupDiv.setAttribute("class", "btn-group");
	groupDiv.setAttribute("role", "group");
	groupDiv.setAttribute("id", "button-matrix-row-1");
	borderDiv.appendChild(groupDiv);
	for (i=1; i<8; i++) {
		var button = document.createElement("button");
		button.setAttribute("class", "btn btn-outline-primary btn-lg");
		button.innerHTML = i;
	button.setAttribute("onclick", "sendThrow(" + button.innerHTML + ")");
		groupDiv.appendChild(button);
	}
	var groupDiv2 = document.createElement("div");
	groupDiv2.setAttribute("class", "btn-group");
	groupDiv2.setAttribute("role", "group");
	groupDiv2.setAttribute("id", "button-matrix-row-2");
	borderDiv.appendChild(groupDiv2);
	for (i=8; i<15; i++) {
		var button = document.createElement("button");
		button.setAttribute("class", "btn btn-outline-primary btn-lg");
		button.innerHTML = i;
	button.setAttribute("onclick", "sendThrow(" + button.innerHTML + ")");
		groupDiv2.appendChild(button);
	}
	var groupDiv3 = document.createElement("div");
	groupDiv3.setAttribute("class", "btn-group");
	groupDiv3.setAttribute("role", "group");
	groupDiv3.setAttribute("id", "button-matrix-row-3");
	borderDiv.appendChild(groupDiv3);
	for (i=15; i<21; i++) {
		var button = document.createElement("button");
		button.setAttribute("class", "btn btn-outline-primary btn-lg");
		button.innerHTML = i;
	button.setAttribute("onclick", "sendThrow(" + button.innerHTML + ")");
		groupDiv3.appendChild(button);
	}
	var button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.innerHTML = "25";
	button.setAttribute("onclick", "sendThrow(" + button.innerHTML + ")");
	groupDiv3.appendChild(button);
	var groupDiv4 = document.createElement("div");
	groupDiv4.setAttribute("class", "btn-group");
	groupDiv4.setAttribute("role", "group");
	groupDiv4.setAttribute("id", "button-matrix-row-4");
	borderDiv.appendChild(groupDiv4);
	var button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.innerHTML = "0";
	button.setAttribute("onclick", "sendThrow(" + button.innerHTML + ")");
	groupDiv4.appendChild(button);
	var button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.setAttribute("data-toggle", "button");
	button.setAttribute("role", "button");
	button.setAttribute("id", "double");
	button.innerHTML = "Double";
	groupDiv4.appendChild(button);
	var button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.setAttribute("data-toggle", "button");
	button.setAttribute("role", "button");
	button.setAttribute("id", "triple");
	button.innerHTML = "Triple";
	groupDiv4.appendChild(button);
}

function drawCricketController() {
	var div = document.getElementById("controls");
	while (div.firstChild) {
		div.removeChild(div.firstChild);
	}
	var borderDiv = document.getElementById("controls");
	var groupDiv = document.createElement("div");
	borderDiv.appendChild(groupDiv);
	groupDiv.setAttribute("class", "btn-group");
	groupDiv.setAttribute("role", "group");
	groupDiv.setAttribute("id", "button-matrix");
	borderDiv.appendChild(groupDiv);
	for (i=15; i<21; i++) {
		var button = document.createElement("button");
		button.setAttribute("class", "btn btn-outline-primary btn-lg");
		button.innerHTML = i;
		button.setAttribute("onclick", "sendThrow(" + button.innerHTML + ")");
		groupDiv.appendChild(button);
	}
	button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.innerHTML = "25";
	button.setAttribute("onclick", "sendThrow(" + button.innerHTML + ")");
	groupDiv.appendChild(button);
	var groupDiv2 = document.createElement("div");
	groupDiv2.setAttribute("class", "btn-group");
	groupDiv2.setAttribute("role", "group");
	groupDiv2.setAttribute("id", "button-matrix-row-2");
	borderDiv.appendChild(groupDiv2);
	button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.innerHTML = "0";
	button.setAttribute("onclick", "sendThrow(" + button.innerHTML + ")");
	groupDiv2.appendChild(button);
	button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.setAttribute("data-toggle", "button");
	button.setAttribute("role", "button");
	button.setAttribute("id", "double");
	button.innerHTML = "Double";
	groupDiv2.appendChild(button);
	button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.setAttribute("data-toggle", "button");
	button.setAttribute("role", "button");
	button.setAttribute("id", "triple");
	button.innerHTML = "Triple";
	groupDiv2.appendChild(button);

}

function nextPlayer() {
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/nextPlayer'), true);
	xhttp.send();
	//location.reload();
}

function drawThrows(playerlist, throwlist) {
	// Draw Table into frame
	var div = document.getElementById("frame");
	while (div.firstChild) {
		div.removeChild(div.firstChild);
	}
	var table = document.createElement("table");
	table.setAttribute("id", "throw-update");
	table.setAttribute("class", "table table-sm table-dark");
	div.appendChild(table);

	// Draw table rows with playername and throws
	for (var player in playerlist) {
		// Split up array
		// arrayPlayer[0] = PlayerID
		// arrayPlayer[1] = PlayerName
		var arrayPlayer = playerlist[player].split(",");

		var tr = document.createElement("tr");
		var tdname = document.createElement("td");
		tdname.setAttribute("id","name-score-" + arrayPlayer[1]);
		tdname.innerHTML = arrayPlayer[1];
		tr.appendChild(tdname);

		//append throws to first table row
		for (var thr in throwlist) {
			for (i=0; i < throwlist[thr].length; i++) {
			    // Split up array
				// throwArray[0] = PlayerID
				// throwArray[1] = ThrowID
				// throwArray[2] = Hit
				// throwArray[3] = Mod
			    var throwArray = throwlist[thr][i].split(",");
				// if playerID matches
				if(throwArray[0] == arrayPlayer[0]) {
					tdbutton = document.createElement("td");
					tdbutton.setAttribute("id", "player-" + arrayPlayer[0] + "-throw-" + throwArray[1]);
					// Pretty output with D for double and T for triple
					var output = ""
					if (throwArray[3] == "2") {
						output += "D";
					}
					else if (throwArray[3] == "3") {
						output += "T";
					}
					output += throwArray[2];
					tdbutton.innerHTML = "<a href=javascript:updateMenu(" + throwArray[1] + ")>" + output + "</a>";
					tr.appendChild(tdbutton);
				}
			}
		}
		table.appendChild(tr);
	}
}

function highlightAndScore(activePlayer, scorelist) {
    var activePlayerDiv = document.getElementById("name-score-" + activePlayer);
	activePlayerDiv.style.border = '5px solid white';
	activePlayerDiv.style.boxShadow = '10px 10px 15px black';
	for (var item in scorelist) {
	    var array = scorelist[item].split(",");
		var playerDiv = document.getElementById("name-score-" + array[0]);
		playerDiv.innerHTML = array[0] + " - " + array[1];
	}
}

function editThrow(throwID, hit) {
	var mod2 = document.querySelector("#doubleModal").getAttribute('aria-pressed');
	var mod3 = document.querySelector("#tripleModal").getAttribute('aria-pressed');
	if (mod2) {
		mod = "2";
	}
	else if (mod3) {
		mod = "3";
	}
	else {
		mod = "1";
	}
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/throw/update/' + throwID + '/' + hit + '/' + mod), true);
	xhttp.send();
	location.reload();
}

function sendThrow(hit) {
	var mod2 = document.querySelector("#double").getAttribute('aria-pressed');
	var mod3 = document.querySelector("#triple").getAttribute('aria-pressed');
	if (mod2) {
		mod = "2";
	}
	else if (mod3) {
		mod = "3";
	}
	else {
		mod = "1";
	}
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			var response = xhttp.responseText;
			if (response.includes("Darts")) {
				xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/nextPlayer'), true);
				xhttp.send();
			}
			//location.reload();
		}
	};
	xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/throw/' + hit + '/' + mod), true);
	xhttp.send();

}

function updateMenu(throwid) {
	// get modal and span
	var modal = document.getElementById("updateModal");
	var span = document.getElementsByClassName("close")[0];
	// get the modal content body
	var divModal = document.getElementById("modal-body");
	// clear body
	while (divModal.firstChild) {
		divModal.removeChild(divModal.firstChild);
	}
	// build up control sequence with throwID in mind (as in Insert Throws)
	var groupDiv = document.createElement("div");
	groupDiv.setAttribute("class", "btn-group");
	groupDiv.setAttribute("role", "group");
	groupDiv.setAttribute("id", "modal-button-matrix-row-1");
	divModal.appendChild(groupDiv);
	for (i=1; i<8; i++) {
		var button = document.createElement("button");
		button.setAttribute("class", "btn btn-outline-primary btn-lg");
		button.innerHTML = i;
		button.setAttribute("onclick", "editThrow(" + throwid + "," + button.innerHTML + ")");
		groupDiv.appendChild(button);
	}
	var groupDiv2 = document.createElement("div");
	groupDiv2.setAttribute("class", "btn-group");
	groupDiv2.setAttribute("role", "group");
	groupDiv2.setAttribute("id", "modal-button-matrix-row-2");
	divModal.appendChild(groupDiv2);
	for (i=8; i<15; i++) {
		var button = document.createElement("button");
		button.setAttribute("class", "btn btn-outline-primary btn-lg");
		button.innerHTML = i;
		button.setAttribute("onclick", "editThrow(" + throwid + "," + button.innerHTML + ")");
		groupDiv2.appendChild(button);
	}
	var groupDiv3 = document.createElement("div");
	groupDiv3.setAttribute("class", "btn-group");
	groupDiv3.setAttribute("role", "group");
	groupDiv3.setAttribute("id", "modal-button-matrix-row-3");
	divModal.appendChild(groupDiv3);
	for (i=15; i<21; i++) {
		var button = document.createElement("button");
		button.setAttribute("class", "btn btn-outline-primary btn-lg");
		button.innerHTML = i;
		button.setAttribute("onclick", "editThrow(" + throwid + "," + button.innerHTML + ")");
		groupDiv3.appendChild(button);
	}
	var button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.innerHTML = "25";
	button.setAttribute("onclick", "editThrow(" + throwid + "," + button.innerHTML + ")");
	groupDiv3.appendChild(button);
	var groupDiv4 = document.createElement("div");
	groupDiv4.setAttribute("class", "btn-group");
	groupDiv4.setAttribute("role", "group");
	groupDiv4.setAttribute("id", "modal-button-matrix-row-4");
	divModal.appendChild(groupDiv4);
	var button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.innerHTML = "0";
	button.setAttribute("onclick", "editThrow(" + throwid + "," + button.innerHTML + ")");
	groupDiv4.appendChild(button);
	var button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.setAttribute("data-toggle", "button");
	button.setAttribute("role", "button");
	button.setAttribute("id", "doubleModal");
	button.innerHTML = "Double";
	groupDiv4.appendChild(button);
	var button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.setAttribute("data-toggle", "button");
	button.setAttribute("role", "button");
	button.setAttribute("id", "tripleModal");
	button.innerHTML = "Triple";
	groupDiv4.appendChild(button);

	// Finally display modal
	modal.style.display = "block";
	// Close handler x
	span.onclick = function() {
		modal.style.display = "none";
	};
	// Handler to click anywhere else
	window.onclick = function(event) {
		if (event.target == modal) {
			modal.style.display = "none";
		}
	}
}

function rematchButton() {
	var nextButton = document.getElementById("nextPlayer");
	nextButton.style.display = "none";
	var button = document.getElementById("rematch");
	button.style.display = "block";
}

function rematch() {
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/rematch'), true);
	xhttp.send();
	location.reload();
}

function drawATC(number) {
	var div = document.getElementById("controls");
	while (div.firstChild) {
		div.removeChild(div.firstChild);
	}
	var borderDiv = document.getElementById("controls");
	var groupDiv = document.createElement("div");
	borderDiv.appendChild(groupDiv);
	groupDiv.setAttribute("class", "btn-group");
	groupDiv.setAttribute("role", "group");
	groupDiv.setAttribute("id", "button-matrix");
	var button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.innerHTML = "Single";
	button.setAttribute("onclick", "sendATC("+ number + ",1)");
	groupDiv.appendChild(button);
	button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.innerHTML = "Double";
	button.setAttribute("onclick", "sendATC(" + number + ",2)");
	groupDiv.appendChild(button);
	button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.innerHTML = "Triple";
	button.setAttribute("onclick", "sendATC(" + number + ",3)");
	groupDiv.appendChild(button);
	var groupDiv2 = document.createElement("div");
	borderDiv.appendChild(groupDiv2);
	groupDiv2.setAttribute("class", "btn-group");
	groupDiv2.setAttribute("role", "group");
	groupDiv2.setAttribute("id", "button-matrix-2");
	button = document.createElement("button");
	button.setAttribute("class", "btn btn-outline-primary btn-lg");
	button.innerHTML = "Miss";
	button.setAttribute("onclick", "sendATC(0,1)");
	groupDiv2.appendChild(button);
}

function highlightATC(activePlayer) {
	var activePlayerDiv = document.getElementById("name-score-" + activePlayer);
	activePlayerDiv.style.border='5px solid white';
	activePlayerDiv.style.boxShadow='10px 10px 15px black';
}

function highlightCricket(activePlayer) {
	var activePlayerDiv = document.getElementById("name-score-" + activePlayer);
	activePlayerDiv.style.border='5px solid white';
	activePlayerDiv.style.boxShadow='10px 10px 15px black';
}

function sendATC(hit,mod) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			var response = xhttp.responseText;
			if (response.includes("Darts")) {
				xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/nextPlayer'), true);
				xhttp.send();
			}
			//location.reload();
		}
	};
	xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/throw/' + hit + '/' + mod), true);
	xhttp.send();
}
