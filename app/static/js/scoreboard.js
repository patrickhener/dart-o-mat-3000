var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    console.log('Websocket connected!');
});

socket.on('refresh', function() {
    window.location.reload(1);
});

socket.on('playSound', function(soundfile) {
    playSound(soundfile);
});

socket.on('drawScoreboardX01', function(list, lastthrowsall, throwsum) {
    drawScoreboardX01(list, lastthrowsall, throwsum);
});

socket.on('drawScoreboardCricket', function(cricketlist, lastthrows) {
    drawScoreboardCricket(cricketlist, lastthrows);
});

socket.on('highlightActiveCricket', function(player, playerID, round, message, throwcount) {
    highlightActiveCricket(player, playerID, round, message, throwcount);
});

socket.on('highlightActive', function(player, playerID, round, message, average, throwcount) {
    highlightActivePlayer(player, playerID, round, message, average, throwcount);
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
        for (item2 in lastthrowsall[item]) {
            var mod = ""
            var array = lastthrowsall[item][item2].split(",");
            var throwDiv = document.getElementById("Throws-" + array[0]);
            var throww = document.createElement("div");
            throww.setAttribute("id", "throw");
            var output = "";
            if (array[2] == "2") {
                output += "D";
            }
            else if (array[2] == "3") {
                output += "T";
            }
            output += array[1];
            throww.innerHTML = "<h2 id='playerThrow'>" + output + "</h2>";
            throwDiv.appendChild(throww);
        }
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
    var divActivePlayer = document.getElementById("header-activePlayer");
    divActivePlayer.innerHTML = activePlayer;
    var divRndcount = document.getElementById("header-rndcount");
    divRndcount.innerHTML = playerRound;
    var divAverage = document.getElementById("header-average");
    divAverage.innerHTML = average;
    var divThrowcount = document.getElementById("header-throwcount");
    divThrowcount.innerHTML = throwcount;
    var messageDiv = document.getElementsByName("Message-" + activePlayer);
    messageDiv[0].innerHTML = "<h1>" + message + "</h1>";
    var throwDiv = document.getElementById("Throws-" + playerID);
};

function playSound(soundfile) {
    if (soundfile != null) {
        var audio = new Audio('http://' + document.domain + ':' + location.port + '/static/sounds/' + soundfile + '.mp3');
        audio.play();
    }
};

function drawScoreboardCricket(list, lastthrows) {
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
        var cricketDiv = document.createElement("div");
        cricketDiv.setAttribute("id", "Cricket-" + list[item].Player);
        borderDiv.appendChild(cricketDiv);
        var cricketTable = document.createElement("table");
        cricketTable.setAttribute("class", "cricketTable");
        cricketDiv.append(cricketTable);
        var cricketArray = list[item].Cricket;
        cricketArray = cricketArray.substr(1);
        cricketArray = cricketArray.substr(0,cricketArray.length - 1);
        // Split array
        // cricketArray[0] = 15
        // cricketArray[1] = 16
        // cricketArray[2] = 17
        // cricketArray[3] = 18
        // cricketArray[4] = 19
        // cricketArray[5] = 20
        // cricketArray[6] = 25
        cricketArray = cricketArray.split(", ");
        for (i=15;i<21;i++) {
            var row = document.createElement("tr");
            var numberColumn = document.createElement("td");
            numberColumn.setAttribute("id", "numberColumn");
            numberColumn.innerHTML = i;
            var countColumn = document.createElement("td");
            countColumn.setAttribute("id", "countColumn");
            if (cricketArray[i - 15] == 0) {
                countColumn.innerHTML = "";
            }
            else if (cricketArray[i - 15] == 1) {
                countColumn.innerHTML = "/";
            }
            else if (cricketArray[i - 15] == 2) {
                countColumn.innerHTML = "X";
            }
            else {
                countColumn.innerHTML = "&#10683;";
            }
            row.appendChild(numberColumn);
            row.appendChild(countColumn);
            cricketTable.appendChild(row);
        }
        var row = document.createElement("tr");
        var numberColumn = document.createElement("td");
        numberColumn.innerHTML = "Bulls";
        var countColumn = document.createElement("td");
        if (cricketArray[6] == 0) {
            countColumn.innerHTML = "";
        }
        else if (cricketArray[6] == 1) {
            countColumn.innerHTML = "/";
        }
        else if (cricketArray[6] == 2) {
            countColumn.innerHTML = "X";
        }
        else {
            countColumn.innerHTML = "&#10683;";
        }
        row.appendChild(numberColumn);
        row.appendChild(countColumn);
        cricketTable.appendChild(row);
        div.appendChild(borderDiv);

        for (var item in lastthrows) {
            for (item2 in lastthrows[item]) {
                var mod = "";
                var array = lastthrows[item][item2].split(",");
                var throwDiv = document.getElementById("Throws-" + array[0]);
                var throww = document.createElement("div");
                throww.setAttribute("id", "throw");
                var output = "";
                if (array[2] == "2") {
                    output += "D";
                }
                else if (array[2] == "3") {
                    output += "T";
                }
                output += array[1];
                throww.innerHTML = "<h2 id='playerThrow'>" + output + "</h2>";
                throwDiv.appendChild(throww);
            }
        }
     }

}

function highlightActiveCricket(activePlayer, playerID, playerRound, message, throwcount) {
    var borderDiv = document.getElementById("Border-" + activePlayer);
    borderDiv.style.border='5px solid white';
    borderDiv.style.boxShadow='10px 10px 15px black';
    var headerLeft = document.getElementById("header-left");
    var divActivePlayer = document.getElementById("header-activePlayer");
    divActivePlayer.innerHTML = activePlayer;
    var divRndcount = document.getElementById("header-rndcount");
    divRndcount.innerHTML = playerRound;
    var divThrowcount = document.getElementById("header-throwcount");
    divThrowcount.innerHTML = throwcount;
    var messageDiv = document.getElementsByName("Message-" + activePlayer);
    messageDiv[0].innerHTML = "<h1>" + message + "</h1>";
    var throwDiv = document.getElementById("Throws-" + playerID);
}

