# General imports
import random
import json

# Import flask dependencies
from flask import Blueprint, request, render_template, url_for, app
from flask_socketio import SocketIO, emit

# Import the database and socketio object from the main app module
from app import db, socketio, IPADDR, PORT

# Import module models
from app.mod_game.models import Game, Player, Score, Cricket, Round, Throw

# Import helper functions
from app.mod_game.helper import clear_db, scoreX01, switchNextPlayer, getPlayingPlayersObjects, getPlayingPlayersID, getScore, checkIfOngoingGame, getActivePlayer, getAverage, getThrows

# Define the blueprint: 'game', set its url prefix: app.url/game
mod_game = Blueprint('game', __name__, url_prefix='/game')

# Routes
@mod_game.route("/")
def index():
    return render_template('/game/index.html', ipaddr=IPADDR, port=PORT)

@mod_game.route("/admin/")
def admin():
    players = Player.query.all()
    return render_template('/game/admin.html', players=players)

@mod_game.route("/manageuser", methods=['GET', 'POST'])
def manageuser():
    # set Things
    created = False
    deleted = False
    players = Player.query.all()
    # If POST (coming from form)
    if request.method == 'POST':
        action = request.form["_action"]
        # Get Action and either add or delete
        if action == "add":
            name = request.form["username"]
            player = Player(name=name, active=False)
            db.session.add(player)
            db.session.commit()
            created = True
        # here comes delete
        elif action == "del":
            name = request.form["delusername"]
            player = Player.query.filter_by(name=name).first()
            db.session.delete(player)
            db.session.commit()
            deleted = True
        # if no action was given
        else:
            created = False
            deleted = False
        # render with fresh player list
        players = Player.query.all()
        return render_template('/game/manageuser.html', created=created, deleted=deleted, name=name, players=players)
    # This one will be taken if it is a GET request
    else:
        return render_template('/game/manageuser.html', created=created, deleted=deleted, players=players)

@mod_game.route("/gameController")
def gameController():
    return render_template('/game/gameController.html')

@mod_game.route("/scoreboardCricket")
def scoreboardCricket():
    game = Game.query.first()
    activePlayer = getActivePlayer()
    #  socketio.emit('refresh')
    return render_template(
        '/game/scoreboardCricket.html',
        player=activePlayer.name,
        gametype=game.gametype,
        variant=game.variant
    )

@mod_game.route("/scoreboardX01")
def scoreboardX01(message=None):
    # Var for returning options
    if not message:
        message = "-"
    else:
        message = message
    # Check if there is a Game ongoing
    started = checkIfOngoingGame()
    # Get general data to draw scoreboard
    playing_players = getPlayingPlayersObjects()
    playing_players_id = getPlayingPlayersID()
    activePlayer = getActivePlayer()
    # getThrows get's you throws like [[round_id,player_id,count],[round_id,player_id,count],[...],[...]]
    throws = getThrows()
    # Get average
    average = getAverage(activePlayer.id)

    game = Game.query.first()
    try:
        rnd = len(Round.query.filter_by(player_id=activePlayer.id).all())
    except:
        rnd = 1

    player_scores = []
    for player in playing_players:
        player_scores.append(getScore(player.id))

    playerScoresList = [{'Player': str(name),'PlayerID': str(playerid), 'Score': str(score)} for name, playerid, score in zip(playing_players,playing_players_id,player_scores)]

    playerRoundThrowList = []
    if not throws:
        playerRoundThrowList = ""
    else:
        for i in range (0, len(throws)):
            playerRoundThrowList.append([{'RoundID': str(throws[i][0]), 'PlayerID': str(throws[i][1]), 'Count': str(throws[i][2])}])

    # playerRoundThrowList will now be something like [[{'RoundID': '1', 'PlayerID': '2', 'Count': '20'}], [{'RoundID': '1', 'PlayerID': '2', 'Count': '20'}], let's feed it to the socket to continue in javascript

    socketio.emit('drawScoreboardX01', playerScoresList)
    socketio.emit('updateThrows', playerRoundThrowList)
    socketio.emit('highlightActive', (activePlayer.name, rnd, message, average))

    return render_template(
        '/game/scoreboardX01.html',
        playerlist=playerScoresList,
        throwlist=playerRoundThrowList,
        message=message,
        average=average,
        started=started,
        player=activePlayer.name,
        gametype=game.gametype,
        rndcount=rnd,
        startIn=game.inGame,
        exitOut=game.outGame
    )

@mod_game.route("/throw/<int:hit>/<int:mod>")
def throw(hit, mod):
    game = Game.query.first()
    # Lookup if next player has to be switched
    if game.nextPlayerNeeded:
        scoreboardX01("Remove Darts")
        return "Switch to next player first\n"
    else:
        # decide which game mechanism to use
        x01_games = ['301','501','701','901']

        if any(x in str(game.gametype) for x in x01_games):
            doIt = scoreX01(hit,mod)
            scoreboardX01(doIt)
            return doIt
        elif str(game.gametype) == "Cricket":
            return "Cricket Game"
        else:
            return "Other Game Type"

@mod_game.route("/nextPlayer")
def nextPlayer():
    doIt = switchNextPlayer()
    game = Game.query.first()
    if game.gametype == "Cricket":
        scoreboardCricket()
    else:
        scoreboardX01(doIt)
    return doIt

@mod_game.route("/endGame")
def endGame():
    clear_db()
    socketio.emit('redirectX01', "/game/")
    socketio.emit('redirectCricket', "/game/")
    return "Done\n"

@socketio.on('startX01')
def on_startX01(data):
    # Flush tables cause for now we handle only one active game
    clear_db()
    # Fill tables
    scorecount = int(data['x01variant'])
    g = Game(gametype=data['x01variant'], inGame=data['startIn'], outGame=data['exitOut'])
    for player in data['players']:
        s = Score(score=scorecount, parkScore=scorecount)
        p = Player.query.filter_by(name=player).first()
        g.players.append(p)
        p.scores.append(s)
        db.session.add(g)
        db.session.add(p)
        db.session.add(s)
        db.session.commit()
    # Determine start Player by random
    a = Player.query.filter_by(name=random.choice(data['players'])).first()
    a.active = True
    # Commit to DB
    db.session.add(a)
    db.session.commit()

    scoreboardX01()
    socketio.emit('redirectIndex', '/game/scoreboardX01')

@socketio.on('startCricket')
def on_startCricket(data):
    # Flush tables cause for now we handle only one active game
    clear_db()
    # Fill tables
    variant = data['variant']
    g = Game(gametype='Cricket',variant=variant)
    for player in data['players']:
        c = Cricket()
        s = Score(score=0, parkScore=0)
        p = Player.query.filter_by(name=player).first()
        g.players.append(p)
        p.crickets.append(c)
        p.scores.append(s)
        db.session.add(g)
        db.session.add(p)
        db.session.add(c)
        db.session.add(s)
        db.session.commit()
    # Determine start Player by random
    a = Player.query.filter_by(name=random.choice(data['players'])).first()
    a.active = True
    # Commit to DB
    db.session.add(a)
    db.session.commit()

    socketio.emit('redirectIndex', '/game/scoreboardCricket')
    scoreboardCricket()
