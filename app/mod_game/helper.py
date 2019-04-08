# Import db from app
from app import db
# Import module models
from app.mod_game.models import Game, Player, Score, Cricket, Round, Throw, LastThrows
# cycle and islice for nextPlayer
from itertools import cycle, islice
# SQLAlchemy functions
from sqlalchemy.sql.expression import func

# Method definitions
def clear_db():
    db.session.query(Game).delete()
    db.session.query(Score).delete()
    db.session.query(Cricket).delete()
    db.session.query(Throw).delete()
    db.session.query(Round).delete()
    db.session.query(LastThrows).delete()

    playingPlayersObject = Player.query.filter_by(game_id=1).all()
    for player in playingPlayersObject:
        player.game_id = None
        player.active = 0

    db.session.commit()

def getActivePlayer():
    activePlayerObject = Player.query.filter_by(active=True).first()
    return activePlayerObject

def getPlayingPlayers():
    playingPlayersObject = Player.query.filter_by(game_id=1).all()
    listOfPlayingPlayers = []
    # Fill in active Players list
    for player in playingPlayersObject:
        listOfPlayingPlayers.append(player.name)

    return listOfPlayingPlayers

def getPlayingPlayersObjects():
    playingPlayersObject = Player.query.filter_by(game_id=1).all()
    return playingPlayersObject

def getPlayingPlayersID():
    playingPlayersObject = Player.query.filter_by(game_id=1).all()
    listOfPlayingPlayersID = []
    # Fill in active Players list
    for player in playingPlayersObject:
        listOfPlayingPlayersID.append(player.id)

    return listOfPlayingPlayersID

def getScore(playerID):
    score = Score.query.filter_by(player_id=playerID).first()
    return score.score

def checkInGame(mod):
    # set active player
    activePlayer = Player.query.filter_by(active=True).first()
    # get Game object
    game = Game.query.first()
    inGame = game.inGame
    playerScore = Score.query.filter_by(player_id=activePlayer.id).first()
    if inGame == "Double":
        if str(playerScore.score) == str(game.gametype):
            if not mod == 2:
                return False
            else:
                return True
        else:
            return True
    elif inGame == "Master":
        if str(playerScore.score) == str(game.gametype):
            if mod == 1:
                return False
            else:
                return True
        else:
            return True
    else:
        return True

def checkOutGame(mod):
    game = Game.query.first()
    outGame = game.outGame
    if outGame == "Double":
        if not mod == 2:
            return False
        else:
            return True
    elif outGame == "Master":
        if mod == 1:
            return False
        else:
            return True
    else:
        return True

def checkOutPossible(newScore):
    game = Game.query.first()
    if not game.outGame == "Straight":
        if newScore == 1:
            return False
        else:
            return True
    else:
        return True

def checkIfOngoingGame():
    if Game.query.filter_by(won=True).first():
        return False
    if Player.query.filter_by(active=True).first():
        return True

    return False

def checkIfOngoingRound(activePlayer):
    # Check if there is a ongoing round associated with player
    ongoing = None
    nextPlayerNeeded = None
    rnd = Round.query.filter_by(player_id=activePlayer.id, ongoing=1).first()

    if not rnd:
        ongoing = False
    else:
        if rnd.throwcount < 3:
            ongoing = True
        else:
            ongoing = False

    return ongoing

def scoreX01(hit,mod):
    # calculate points to be substracted from score
    points = hit * mod
    # check if there is a game going on
    if checkIfOngoingGame():
        # set active player
        activePlayer = Player.query.filter_by(active=True).first()
        # get Game object
        game = Game.query.first()
        # Check if there is a ongoing round associated, if not create a new one
        if not checkIfOngoingRound(activePlayer):
            if (LastThrows.query.filter_by(player_id=activePlayer.id).all()):
                LastThrows.query.filter_by(player_id=activePlayer.id).delete()
                db.session.commit()
            rnd = Round(player_id=activePlayer.id,ongoing=True,throwcount=0)
            db.session.add(rnd)
            db.session.commit()
        else:
            # Set round object
            rnd = Round.query.filter_by(player_id=activePlayer.id, ongoing=1).first()

        # Check if ongoing round is over
        if rnd.throwcount == 3:
            game.nextPlayerNeeded = True
        else:
            # set throwcount and old score
            throwcount = rnd.throwcount
            playerScore = Score.query.filter_by(player_id=activePlayer.id).first()
            # check if bust
            if playerScore.score - points < 0:
                game.nextPlayerNeeded = True
                throwcount += 1
                rnd.throwcount = throwcount
                #rnd.throwcount = 3
                playerScore.score = playerScore.parkScore
                db.session.commit()
                return "Bust! Remove Darts!"
            # check if won
            elif playerScore.score - points == 0:
                # TODO Here might be the best place to implement statistics function
                #
                if checkOutGame(mod):
                    game.won = True
                    throwcount += 1
                    rnd.throwcount = throwcount
                    playerScore.score = 0
                    db.session.commit()
                    return "Winner!"
                else:
                    game.nextPlayerNeeded = True
                    throwcount +=1
                    rnd.throwcount = throwcount
                    playerScore.score = playerScore.parkScore
                    db.session.commit()
                    return "Bust! " + game.outGame + " out!"
            # define new score, increase throwcount, commit to db
            else:
                result = "-"
                newScore = playerScore.score - points
                if not checkOutPossible(newScore):
                    throwcount += 1
                    rnd.throwcount = throwcount
                    playerScore.score = playerScore.parkScore
                    game.nextPlayerNeeded = True
                    db.session.commit()
                    result = "No Out possible! Remove Darts!"
                else:
                    throwcount += 1
                    if checkInGame(mod):
                        playerScore.score = newScore
                    else:
                        result = str(game.inGame) + " in!"
                    rnd.throwcount = throwcount
                    throw = Throw(hit=hit,mod=mod,round_id=rnd.id,player_id=activePlayer.id)
                    if throwcount == 3:
                        playerScore.parkScore = newScore
                        game.nextPlayerNeeded = True
                        result = "Remove Darts!"
                    db.session.add(throw)
                    db.session.commit()

                newLastThrow = LastThrows(player_id=activePlayer.id, counts=points)
                db.session.add(newLastThrow)
                db.session.commit()

                return result
    else:
        # Output if no game is running
        return "There is no active game running\n"

def switchNextPlayer():
    # First check if the game was won
    game = Game.query.first()
    if game.won:
        return "There is no active game running"
    else:
        # Then set active Player round ongoing to 0 and nextPlayerNeeded in Game to 0
        activePlayerObject = getActivePlayer()
        activePlayerObject = Player.query.filter_by(active=True).first()
        activePlayerRound = Round.query.filter_by(player_id=activePlayerObject.id, ongoing=1).first()
        activePlayerRound.ongoing = False
        game.nextPlayerNeeded = False
        # Initialize variables to work with
        key = []
        listOfPlayingPlayers = getPlayingPlayers()
        # Find key of active player in list
        for i, x in enumerate(listOfPlayingPlayers):
            if x == str(activePlayerObject):
                positionInListOfActivePlayer = i
        # Fill a list from 0 to x as long as the list of active players
        for x in range (0, len(listOfPlayingPlayers)):
            key.append(x)
        # define cycle over key list
        cyclePlayerKeyInList = cycle(key)
        # start at position of active player in the keyList
        positionKeyAfterActivePlayerKey = islice(cyclePlayerKeyInList, positionInListOfActivePlayer+1, None)
        # Take one step in list and define next player with the resulting key
        nextPlayerKeyInList = next(positionKeyAfterActivePlayerKey)
        nextActivePlayerObject = Player.query.filter_by(name=listOfPlayingPlayers[nextPlayerKeyInList]).first()
        # Commit current active player false and next active player true to database
        activePlayerObject.active = False
        nextActivePlayerObject.active = True
        db.session.commit()

        return "-"

def getAverage(playerID):
    throws = (Throw.query.filter_by(player_id=playerID)).all()
    if not throws:
        return str(0)
    else:
        throwlist = []
        for throw in throws:
            throwlist.append(str(throw))
        throwlist = [float(s) for s in throwlist]
        avgofthrows = round((sum(throwlist) / len(throwlist)), 2)
        return str(avgofthrows)

def getThrowsCount(playerID):
    throws = (Throw.query.filter_by(player_id=playerID)).all()
    if throws == []:
        return "0"
    else:
        return len(throws)

def getLastThrows(playerID):
    return LastThrows.query.filter_by(player_id=playerID).all()

def getAllLastThrows():
    return LastThrows.query.all()
