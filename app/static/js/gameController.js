var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
     console.log('Websocket connected!');
});

socket.on('redirectGameController', function(url) {
	window.location.href = url;
});

socket.on('drawX01Controller', function() {
	drawX01Controller();
});

socket.on('drawThrowContainer', function(playerlist) {
	drawThrowContainer(playerlist);
});

socket.on('drawThrows', function(throwlist) {
	drawThrows(throwlist);
});

function drawX01Controller() {
	var borderDiv = document.getElementById("x01-controls");
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
};

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

			if (response !== "-") {
				xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/nextPlayer'), true);
				xhttp.send();
			}
			location.reload();
		}
	};
	xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/throw/' + hit + '/' + mod), true);
	xhttp.send();

};

function endGame() {
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/endGame'), true);
	xhttp.send();
};

function drawThrowContainer(playerlist) {
	for (var item in playerlist) {
		var array = playerlist[item].split(",");
		var borderDiv = document.createElement("div");
		borderDiv.setAttribute("id", "border-" + array[0]);
		borderDiv.setAttribute("class", "col");
		var divThrows = document.getElementById("throws");
		var grpDiv = document.createElement("div");
		grpDiv.setAttribute("class", "btn-group");
		grpDiv.setAttribute("id", "btn-group-" + array[0]);
		grpDiv.innerHTML = "<h1 id='h1-throws'>" + array[1] + "</h1>";
		divThrows.appendChild(borderDiv);
		borderDiv.appendChild(grpDiv);
		// var divPlayerThrows = document.createElement("div");
		// divPlayerThrows.setAttribute("id", "Throws-" + array[0]);
		// grpDiv.appendChild(divPlayerThrows);
	}
};

function drawThrows(throwlist) {
	console.log(throwlist);
	for (var item in throwlist) {
		var array = throwlist[item].split(",");
		var divPlayerThrows = document.getElementById("btn-group-" + array[0]);
		var throww = document.createElement("button");
		throww.setAttribute("class", "btn btn-outline-primary btn-lg");
		throww.setAttribute("data-toggle", "button");
		throww.setAttribute("role", "button");
		throww.setAttribute("id","throw-id-" + array[1]);
		var output = "";
		if (array[3] == "2") {
			output += "D";
		}
		else if (array[3] == "3") {
			output += "T";
		}
		output += array[2];
		throww.innerHTML = output;
		divPlayerThrows.appendChild(throww);
	}
};

function editThrow(throwID, hitString) {

}
