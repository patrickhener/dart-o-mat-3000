var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
     console.log('Websocket connected!');
});

socket.on('redirectIndex', function(url) {
	console.log("Got redirected")
	window.location.href = url;
});
