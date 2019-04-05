// Socket Settings
var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
     console.log('Websocket connected!');
});

socket.on('refresh', function() {
	window.location.reload(1);
});

socket.on('drawScoreboardX01', function(playerScoresList, activePlayer) {
	console.log("Drawing")
	createDivFromJSON(playerScoresList);
	highlightActivePlayer(activePlayer);
});

// Functions
function createDivFromJSON(json) {
	var col = [];
	for (var i = 0; i < json.length; i++) {
	    for (var key in json[i]) {
		if (col.indexOf(key) === -1) {
		    col.push(key);
		}
	    }
	}
	alert(col)

	var div = document.createElement("div");
	div.setAttribute('name','scores');

	var table = document.createElement("table");
	table.setAttribute('class','table table-striped table-dark');
	var tr = table.insertRow(-1);
	for (var i = 0; i < col.length; i++) {
		var th = document.createElement("th");
		th.innerHTML = col[i];
	    tr.appendChild(th);
	}

	for (var i = 0; i < json.length; i++) {

	    tr = table.insertRow(-1);

	    for (var j = 0; j < col.length; j++) {
		var tabCell = tr.insertCell(-1);
		tabCell.innerHTML = json[i][col[j]];
		console.log(json[i][col[j]])
	    }
	}

	// var divContainer = document.getElementById("content");
	// divContainer.innerHTML = "";
	// divContainer.appendChild(div);
};

function highlightActivePlayer(activePlayer) {
	var name = activePlayer;
	console.log(name)
};
