# General helper file

# Import db from app
from app import db
# cycle and islice for nextPlayer
from itertools import cycle, islice
# Babel Translation
from flask_babel import gettext

# Import module models
from .models import Game, Player, Score, Cricket, Round, Throw, CricketControl, PointsGained, ATC, Podium, Split


# Method definitions
def clear_db():
    db.session.query(Game).delete()
    db.session.query(Score).delete()
    db.session.query(Cricket).delete()
    db.session.query(Throw).delete()
    db.session.query(Round).delete()
    db.session.query(CricketControl).delete()
    db.session.query(PointsGained).delete()
    db.session.query(ATC).delete()
    db.session.query(Podium).delete()
    db.session.query(Split).delete()

    playing_players_object = Player.query.filter_by(game_id=1).all()
    for player in playing_players_object:
        player.game_id = None
        player.out = None
        player.active = 0

    db.session.commit()


def get_active_player():
    active_player_object = Player.query.filter_by(active=True).first()
    return active_player_object


def get_playing_players():
    playing_players_object = Player.query.filter_by(game_id=1).all()
    list_of_playing_players = []
    # Fill in active Players list
    for player in playing_players_object:
        list_of_playing_players.append(player.name)

    return list_of_playing_players


def get_playing_players_not_out():
    playing_players_object = Player.query.filter_by(game_id=1, out=0).all()
    list_of_playing_players = []
    # Fill in active Players list
    for player in playing_players_object:
        list_of_playing_players.append(player.name)

    return list_of_playing_players


def get_playing_players_not_out_objects():
    playing_players_object = Player.query.filter_by(game_id=1, out=0).all()
    return playing_players_object


def get_playing_players_objects():
    playing_players_object = Player.query.filter_by(game_id=1).all()
    return playing_players_object


def get_playing_players_id():
    playing_players_object = Player.query.filter_by(game_id=1).all()
    list_of_playing_players_id = []
    # Fill in active Players list
    for player in playing_players_object:
        list_of_playing_players_id.append(player.id)

    return list_of_playing_players_id


def get_score(player_id):
    score = Score.query.filter_by(player_id=player_id).first()
    return score.score


def check_other_players():
    players = Player.query.filter_by(out=False).all()
    return len(players)


def check_if_ongoing_game():
    if Game.query.filter_by(won=True).first():
        return False
    if Player.query.filter_by(active=True).first():
        return True

    return False


def check_if_ongoing_round(active_player):
    # Check if there is a ongoing round associated with player
    rnd = Round.query.filter_by(player_id=active_player.id, ongoing=1).first()

    if not rnd:
        ongoing = False
    else:
        if rnd.throwcount < 3:
            ongoing = True
        else:
            ongoing = False

    return ongoing


def switch_next_player():
    # First check if the game was won
    game = Game.query.first()
    if game.won:
        return gettext(u"There is no active game running")
    else:
        # Then set active Player round ongoing to 0 and nextPlayerNeeded in Game to 0
        active_player_object = Player.query.filter_by(active=True).first()
        # else just switch player as always
        active_player_round = Round.query.filter_by(player_id=active_player_object.id, ongoing=1).first()
        try:
            active_player_round.ongoing = False
        except AttributeError:
            print("Error handled, lolz.")
        game.nextPlayerNeeded = False
        # Initialize variables to work with
        key = []
        list_of_playing_players = get_playing_players_not_out()
        # Find key of active player in list
        for i, x in enumerate(list_of_playing_players):
            if x == str(active_player_object):
                position_list_active_player = i
        # Fill a list from 0 to x as long as the list of active players
        for x in range(0, len(list_of_playing_players)):
            key.append(x)
        # define cycle over key list
        cycle_player_key_in_list = cycle(key)
        # start at position of active player in the keyList
        position_key_after_active = islice(cycle_player_key_in_list, position_list_active_player+1, None)
        # Take one step in list and define next player with the resulting key
        next_player_key = next(position_key_after_active)
        next_active_player_object = Player.query.filter_by(name=list_of_playing_players[next_player_key]).first()
        # Commit current active player false and next active player true to database
        active_player_object.active = False
        next_active_player_object.active = True
        db.session.commit()

        return "-"


def get_average(player_id):
    throws = (Throw.query.filter_by(player_id=player_id)).all()
    rnds = (Round.query.filter_by(player_id=player_id)).all()
    if not throws:
        return str(0)
    else:
        throwlist = []
        roundlist = []
        for throw in throws:
            throwlist.append(str(throw))
        for rnd in rnds:
            roundlist.append(rnd.id)
        throwlist = [float(s) for s in throwlist]
        avgofthrows = round((sum(throwlist) / len(roundlist)), 2)
        return str(avgofthrows)


def get_throws_count(player_id):
    throws = (Throw.query.filter_by(player_id=player_id)).all()
    # if throws == []:
    if not throws:
        return "0"
    else:
        return len(throws)


def get_last_throws(player_id):
    throwlist = []
    last_round = Round.query.filter_by(player_id=player_id).order_by(Round.id.desc()).first()
    # if last_round == None:
    if not last_round:
        throwlist.append(str(player_id) + ",0,0")
        throwlist.append(str(player_id) + ",0,0")
        throwlist.append(str(player_id) + ",0,0")
    else:
        last_throws = Throw.query.filter_by(round_id=last_round.id).all()
        if not last_throws == []:
            try:
                for i in range(0, 3):
                    throwlist.append(str(player_id) + "," + str(last_throws[i].id) + "," + str(last_throws[i].hit)
                                     + "," + str(last_throws[i].mod))
            except:
                print("Exception handled, lolz")
        else:
            throwlist.append(str(player_id) + ",0,0")
            throwlist.append(str(player_id) + ",0,0")
            throwlist.append(str(player_id) + ",0,0")

    return throwlist


def get_last_throws_count():
    game = Game.query.first()
    if not game:
        return "No Game is running."
    else:
        player = get_active_player()
        last_round = Round.query.order_by(Round.id.desc()).first()
        throwcount = 0
        # if last_round == None:
        if not last_round:
            return throwcount
        else:
            last_throws = Throw.query.filter_by(round_id=last_round.id).all()
            if not last_throws == []:
                if player.id == last_round.player_id:
                    throwcount = len(last_throws)
                else:
                    throwcount = 0
            else:
                throwcount = 0

            return throwcount


def get_all_throws(player_id):
    throws = (Throw.query.filter_by(player_id=player_id)).all()
    return throws


def set_podium(player_id):
    # Get Podium Objects
    podium = Podium.query.all()
    # Get Player Object
    player = Player.query.filter_by(id=player_id).first()
    # If there are any Objects
    if podium:
        p = Podium(place=len(podium)+1, name=player.name, player_id=player_id)
    # No Objects yet, so 1st Place
    else:
        p = Podium(place=1, name=player.name, player_id=player_id)

    switch_next_player()

    player.out = True
    player.active = False
    db.session.add(p)
    db.session.commit()

    return "Done"


def set_last_podium():
    # Get Podium Objects
    podium = Podium.query.all()
    # Get looser player
    looser = Player.query.filter_by(game_id=1, out=0).first()
    p = Podium(place=len(podium)+1, name=looser.name, player_id=looser.id)
    looser.out = True
    db.session.add(p)
    db.session.commit()

    return "Done"


def update_throw_and_score(throw, hit, mod, add):
    # get Throw and score
    score = Score.query.filter_by(player_id=throw.player_id).first()
    # Calculate old points resulting of old throw
    oldpoints = throw.hit * throw.mod
    # Calculate new points resulting of altered throw
    newpoints = int(hit) * int(mod)
    # Calculate difference
    alter_score = newpoints - oldpoints
    # Calculate new score
    if add:
        new_score = score.score + alter_score
    else:
        new_score = score.score - alter_score
    # Set Throw to new values
    throw.hit = int(hit)
    throw.mod = int(mod)
    # Set Score and Park Score to new Score
    score.score = new_score
    # Commit to db
    db.session.commit()

    return "Done"
