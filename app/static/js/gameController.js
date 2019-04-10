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
	var div = document.getElementById("x01-controls");
	while (div.firstChild) {
		div.removeChild(div.firstChild);
	}
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

function nextPlayer() {
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/nextPlayer'), true);
	xhttp.send();
	location.reload();
}

function drawThrowContainer(playerlist) {
	var div = document.getElementById("frame");
	while (div.firstChild) {
		div.removeChild(div.firstChild);
	}
	var frameDiv = document.getElementById("frame");
	for (var item in playerlist) {
		var array = playerlist[item].split(",");
		var borderDiv = document.createElement("div");
		borderDiv.setAttribute("id", "border-" + array[0]);
		// borderDiv.setAttribute("class", "row");
		frameDiv.appendChild(borderDiv);
		var headerDiv = document.createElement("div");
		headerDiv.setAttribute("id", "header");
		// headerDiv.setAttribute("class", "col");
		headerDiv.innerHTML = "<b>" + array[1] + "</b>";
		borderDiv.appendChild(headerDiv);
		var grpDiv = document.createElement("div");
		grpDiv.setAttribute("class", "btn-group");
		grpDiv.setAttribute("id", "btn-group-" + array[0]);
		borderDiv.appendChild(grpDiv);
	}
};

function drawThrows(throwlist) {
	for (var item in throwlist) {
		var array = throwlist[item].split(",");
		var divPlayerThrows = document.getElementById("btn-group-" + array[0]);
		var dropdownDiv = document.createElement("div");
		dropdownDiv.setAttribute("class", "dropdown");
		divPlayerThrows.appendChild(dropdownDiv);


		var throww = document.createElement("button");
		throww.setAttribute("class", "btn btn-outline-primary btn-lg dropdown-toggle");
		throww.setAttribute("type", "button");

		throww.setAttribute("data-toggle", "dropdown");
		throww.setAttribute("aria-haspopup", "true");
		throww.setAttribute("aria-expanded", "false");
		throww.setAttribute("id","dropdownMenuButton-" + array[1]);
		var output = "";
		if (array[3] == "2") {
			output += "D";
		}
		else if (array[3] == "3") {
			output += "T";
		}
		output += array[2];
		throww.innerHTML = output;
		dropdownDiv.appendChild(throww);
		var dropdownMenuDiv = document.createElement("div");
		dropdownMenuDiv.setAttribute("class", "dropdown-menu");
		dropdownMenuDiv.setAttribute("aria-labelledby", "dropdownMenuButton-" + array[1]);
		dropdownDiv.appendChild(dropdownMenuDiv);
		var link = document.createElement("button");
		link.setAttribute("class", "dropdown-item");
		link.setAttribute("onclick", "editThrow(" + array[1] + ",'0','1')");
		link.innerHTML = "0";
		dropdownMenuDiv.appendChild(link);
		var divider = document.createElement("div");
		divider.setAttribute("class", "dropdown-divider");
		dropdownMenuDiv.appendChild(divider);
		for (i=1; i<21; i++) {
			var link = document.createElement("button");
			link.setAttribute("class", "dropdown-item");
			link.setAttribute("onclick", "editThrow(" + array[1] + "," + i + ",1)");
			link.innerHTML = i;
			dropdownMenuDiv.appendChild(link);
		}
		var link = document.createElement("button");
		link.setAttribute("class", "dropdown-item");
		link.setAttribute("onclick", "editThrow(" + array[1] + ",'25','1')");
		link.innerHTML = "25";
		dropdownMenuDiv.appendChild(link);
		var divider = document.createElement("div");
		divider.setAttribute("class", "dropdown-divider");
		dropdownMenuDiv.appendChild(divider);
		for (i=1; i<21; i++) {
			var link = document.createElement("button");
			link.setAttribute("class", "dropdown-item");
			link.setAttribute("onclick", "editThrow(" + array[1] + "," + i + ",2)");
			link.innerHTML = "D" + i;
			dropdownMenuDiv.appendChild(link);
		}
		var link = document.createElement("button");
		link.setAttribute("class", "dropdown-item");
		link.setAttribute("onclick", "editThrow(" + array[1] + ",'25','2')");
		link.innerHTML = "D25";
		dropdownMenuDiv.appendChild(link);
		var divider = document.createElement("div");
		divider.setAttribute("class", "dropdown-divider");
		dropdownMenuDiv.appendChild(divider);
		for (i=1; i<21; i++) {
			var link = document.createElement("button");
			link.setAttribute("class", "dropdown-item");
			link.setAttribute("onclick", "editThrow(" + array[1] + "," + i + ",'3')");
			link.innerHTML = "T" + i;
			dropdownMenuDiv.appendChild(link);
		}

	}
};

function editThrow(throwID, hit, mod) {
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", ('http://' + document.domain + ':' + location.port + '/game/throw/update/' + throwID + '/' + hit + '/' + mod), true);
	xhttp.send();
	location.reload();
};
