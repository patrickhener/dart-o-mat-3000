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

socket.on('drawScoreboardCricket', function(cricketlist, lastthrows, closed) {
    drawScoreboardCricket(cricketlist, lastthrows, closed);
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
            throwDiv = document.getElementById("Throws-" + array[0]);
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
        sumDiv = document.getElementById("Sum-" + array[0]);
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

function drawScoreboardCricket(list, lastthrows, closed) {
    // Format Lastthrows list
    lastthrows = lastthrows.substring(2);
    lastthrows = lastthrows.substring(0, lastthrows.length - 2);
    lastthrows = lastthrows.split("], [");
    var div = document.getElementById("score");
    while (div.firstChild) {
        div.removeChild(div.firstChild);
    }
    var divCount = 0;
    for (var item in list) {
        if (divCount == 2) {
           var linebrakeDiv = document.createElement("div");
           linebrakeDiv.setAttribute("class", "w-100");
           div.appendChild(linebrakeDiv);
           divCount = 0;
        }
        // create border div for player
        var borderDiv = document.createElement("div");
        borderDiv.setAttribute("id", "Cricket-Border-" + list[item].Player);
        borderDiv.setAttribute("class", "col");
        // create player Table
        var playerTable = document.createElement("table");
        playerTable.setAttribute("id", "playerTable-" + list[item].Player);
        borderDiv.appendChild(playerTable);
        // Create name Row
        var nameRow = document.createElement("tr");
        playerTable.appendChild(nameRow);
        // Write name to row
        var playerNameColumn = document.createElement("td");
        playerNameColumn.setAttribute("id", "playerNameColumn");
        playerNameColumn.innerHTML = "<h2 id='playerName'>" + list[item].Player + "</h2>";
        nameRow.appendChild(playerNameColumn);
        // Cricket array for symbol row (and numbers later on)
        var cricketArray = list[item].Cricket;
        cricketArray = cricketArray.substring(1);
        cricketArray = cricketArray.substring(0,cricketArray.length - 1);
        // Split array
        // cricketArray[0] = 15
        // cricketArray[1] = 16
        // cricketArray[2] = 17
        // cricketArray[3] = 18
        // cricketArray[4] = 19
        // cricketArray[5] = 20
        // cricketArray[6] = 25
        cricketArray = cricketArray.split(", ");
        // append 15 to 20 symbol row
        for (i=15;i<22;i++) {
                var countColumn = document.createElement("td");
                countColumn.setAttribute("rowspan", "2");
                countColumn.setAttribute("name", "c" + i);
                countColumn.setAttribute("id", "countColumn");
                if (cricketArray[i - 15] == 0) {
                    countColumn.innerHTML = "";
                }
                else if (cricketArray[i - 15] == 1) {
                    countColumn.innerHTML = "<h2>/</h2>";
                }
                else if (cricketArray[i - 15] == 2) {
                    countColumn.innerHTML = "<h2>X</h2>";
                }
                else {
                    countColumn.innerHTML = "<h2>&#10683;</h2>";
                }
                nameRow.appendChild(countColumn);
        }
        // append Bulls Symbol row
        countColumn.setAttribute("rowspan", "2");
        countColumn.setAttribute("name", "c25");
        countColumn.setAttribute("id", "countColumn");
        if (cricketArray[6] == 0) {
            countColumn.innerHTML = "";
        }
        else if (cricketArray[6] == 1) {
            countColumn.innerHTML = "<h2>/</h2>";
        }
        else if (cricketArray[6] == 2) {
            countColumn.innerHTML = "<h2>X</h2>";
        }
        else {
            countColumn.innerHTML = "<h2>&#10683;</h2>";
        }
        nameRow.appendChild(countColumn);
        // Create score row and column
        var scoreRow = document.createElement("tr");
        playerTable.appendChild(scoreRow);
        var scoreColumn = document.createElement("td");
        scoreColumn.setAttribute("id", "playerScoreColumn");
        scoreColumn.innerHTML = "<h2 id='playerScore'>" + list[item].Score + "</h2>";
        scoreRow.appendChild(scoreColumn);
        // Create next table row with message field and numbers
        var messageRow = document.createElement("tr");
        playerTable.appendChild(messageRow);
        var messageColumn = document.createElement("td");
        messageColumn.setAttribute("id", "Message-" + list[item].Player);
        messageRow.appendChild(messageColumn);
        // Append number 15 to 20 to table
        for (i=15;i<22;i++) {
            var numberColumn = document.createElement("td");
            numberColumn.setAttribute("rowspan", "2");
            numberColumn.setAttribute("name", "n" + i);
            numberColumn.setAttribute("id", "numberColumn");
            numberColumn.innerHTML = "<h2>" + i + "</h2>";
            messageRow.appendChild(numberColumn);
        }
        // Append bulls to table
        numberColumn.setAttribute("rowspan", "2");
        numberColumn.setAttribute("name", "n25");
        numberColumn.setAttribute("id", "numberColumn");
        numberColumn.innerHTML = "<h2>Bulls</h2>";
        messageRow.appendChild(numberColumn);
        // Create lastthrows row
        var lastThrowsRow = document.createElement("tr");
        playerTable.appendChild(lastThrowsRow);
        var lastThrowsColumn  = document.createElement("td");
        lastThrowsColumn.setAttribute("id", "playerLastThrows");
        // Insert Last Throws in column
        var output = "";
        var playerLastThrows = lastthrows[item].split(", ");
        for (var item2 in playerLastThrows) {
            var throwArray = playerLastThrows[item2].substring(1);
            throwArray = throwArray.substring(0, throwArray.length - 1);
            throwArray = throwArray.split(",");
            // throwArray[0] = playerID
            // throwArray[1] = hit
            // throwArray[2] = mod
            if (throwArray[2] == "2") {
                output += "D";
            }
            else if (throwArray[2] == "3") {
                output += "T";
            }
            output += throwArray[1];
            output += " ";
        }
        lastThrowsColumn.innerHTML = "<h2>" + output + "</h2>";
        lastThrowsRow.appendChild(lastThrowsColumn);
        // Append border Div
        div.appendChild(borderDiv);
        // Count linebrake up
        divCount += 1;
     }

    // Closed marking
    // Format List
    closed = closed.toString();
    closed = closed.substring(1);
    closed = closed.substring(0, closed.length - 1);
    closed = closed.split(", ");
    // Loop through and search cXX
    for (var item in closed) {
        var itemToChange = closed[item].substring(1).toString();
        itemToChange = itemToChange.substring(0, itemToChange.length - 1);
        var elementListToChange = document.getElementsByName("c" + itemToChange);
        for (i=0; i<elementListToChange.length; i++) {
            elementListToChange[i].style.display = "none";
        }
        elementListToChange = document.getElementsByName("n" + itemToChange);
        for (i=0; i<elementListToChange.length; i++) {
            elementListToChange[i].style.display = "none";
        }
    }
}

function highlightActiveCricket(activePlayer, playerID, playerRound, message, throwcount) {
    var borderDiv = document.getElementById("Cricket-Border-" + activePlayer);
    borderDiv.style.border='5px solid white';
    borderDiv.style.boxShadow='10px 10px 15px black';
    var divActivePlayer = document.getElementById("header-activePlayer");
    divActivePlayer.innerHTML = activePlayer;
    var divRndcount = document.getElementById("header-rndcount");
    divRndcount.innerHTML = playerRound;
    var divThrowcount = document.getElementById("header-throwcount");
    divThrowcount.innerHTML = throwcount;
    var messageColumn = document.getElementById("Message-" + activePlayer);
    messageColumn.innerHTML = "<h2>" + message + "</h2>";
}