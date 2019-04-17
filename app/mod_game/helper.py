# Import db from app
from app import db
# Import module models
from app.mod_game.models import Game, Player, Score, Cricket, Round, Throw, CricketControl
# cycle and islice for nextPlayer
from itertools import cycle, islice
# Babel Translation
from flask_babel import gettext


# Method definitions
def clear_db():
    db.session.query(Game).delete()
    db.session.query(Score).delete()
    db.session.query(Cricket).delete()
    db.session.query(Throw).delete()
    db.session.query(Round).delete()
    db.session.query(CricketControl).delete()

    playing_players_object = Player.query.filter_by(game_id=1).all()
    for player in playing_players_object:
        player.game_id = None
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


def get_cricket(player_id):
    cricket = Cricket.query.filter_by(player_id=player_id).first()
    return cricket


def check_in_game(mod):
    # set active player
    active_player = Player.query.filter_by(active=True).first()
    # get Game object
    game = Game.query.first()
    in_game = game.inGame
    player_score = Score.query.filter_by(player_id=active_player.id).first()
    if in_game == "Double":
        if str(player_score.score) == str(game.gametype):
            if not mod == 2:
                return False
            else:
                return True
        else:
            return True
    elif in_game == "Master":
        if str(player_score.score) == str(game.gametype):
            if mod == 1:
                return False
            else:
                return True
        else:
            return True
    else:
        return True


def check_out_game(mod):
    game = Game.query.first()
    out_game = game.outGame
    if out_game == "Double":
        if not mod == 2:
            return False
        else:
            return True
    elif out_game == "Master":
        if mod == 1:
            return False
        else:
            return True
    else:
        return True


def check_out_possible(new_score):
    game = Game.query.first()
    if not (game.outGame == "Straight"):
        if not (game.outGame == "Direkt"):
            if new_score == 1:
                return False
            else:
                return True
        else:
            return True
    else:
        return True


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


def update_throw_table(throw_id, hit, mod):
    game = Game.query.first()
    if game.gametype == "Cricket":
        # get Throw and score
        throw = (Throw.query.filter_by(id=throw_id)).first()
        # TODO Implement Change Method here

    else:
        # get Throw and score
        throw = (Throw.query.filter_by(id=throw_id)).first()
        score = (Score.query.filter_by(player_id=throw.player_id)).first()
        # Calculate old points resulting of old throw
        oldpoints = throw.hit * throw.mod
        # Calculate new points resulting of altered throw
        newpoints = int(hit) * int(mod)
        # Calculate difference
        alter_score = newpoints - oldpoints
        # Calculate new score
        new_score = score.score - alter_score
        # Set Throw to new values
        throw.hit = int(hit)
        throw.mod = int(mod
                        )
        # Set Score and Park Score to new Score
        score.score = new_score
        score.parkScore = new_score
        # Commit to db
        db.session.commit()
    return "-"


def score_x01(hit, mod):
    # calculate points to be substracted from score
    points = hit * mod
    # check if there is a game going on
    if check_if_ongoing_game():
        # set active player
        active_player = Player.query.filter_by(active=True).first()
        # get Game object
        game = Game.query.first()
        # Check if there is a ongoing round associated, if not create a new one
        if not check_if_ongoing_round(active_player):
            rnd = Round(player_id=active_player.id, ongoing=True, throwcount=0)
            db.session.add(rnd)
            db.session.commit()
        else:
            # Set round object
            rnd = Round.query.filter_by(player_id=active_player.id, ongoing=1).first()

        # Check if ongoing round is over
        if rnd.throwcount == 3:
            game.nextPlayerNeeded = True
        else:
            # set throwcount and old score
            throwcount = rnd.throwcount
            player_score = Score.query.filter_by(player_id=active_player.id).first()
            # check if bust
            if player_score.score - points < 0:
                game.nextPlayerNeeded = True
                throwcount += 1
                rnd.throwcount = throwcount
                player_score.score = player_score.parkScore
                db.session.commit()
                return gettext(u"Bust! Remove Darts!")
            # check if won
            elif player_score.score - points == 0:
                # TODO Here might be the best place to implement statistics function
                #
                if check_out_game(mod):
                    game.won = True
                    throwcount += 1
                    rnd.throwcount = throwcount
                    player_score.score = 0
                    db.session.commit()
                    return gettext(u"Winner!")
                else:
                    game.nextPlayerNeeded = True
                    throwcount += 1
                    rnd.throwcount = throwcount
                    player_score.score = player_score.parkScore
                    db.session.commit()
                    return gettext(u"Bust! %(mode)s out!", mode=game.outGame)
            # define new score, increase throwcount, commit to db
            else:
                result = "-"
                new_score = player_score.score - points
                if not check_out_possible(new_score):
                    throwcount += 1
                    rnd.throwcount = throwcount
                    player_score.score = player_score.parkScore
                    game.nextPlayerNeeded = True
                    db.session.commit()
                    result = gettext(u"No Out possible! Remove Darts!")
                else:
                    throwcount += 1
                    if check_in_game(mod):
                        player_score.score = new_score
                    else:
                        result = str(game.inGame) + " in!"
                    rnd.throwcount = throwcount
                    throw = Throw(hit=hit, mod=mod, round_id=rnd.id, player_id=active_player.id)
                    if throwcount == 3:
                        player_score.parkScore = new_score
                        game.nextPlayerNeeded = True
                        result = gettext(u"Remove Darts!")
                    db.session.add(throw)
                    db.session.commit()

                return result
    else:
        # Output if no game is running
        return gettext("There is no active game running")


def score_cricket(hit, mod):
    # Empty result for now
    result = ""
    # Check if game is ongoing
    if check_if_ongoing_game():
        # set active player
        active_player = Player.query.filter_by(active=True).first()
        # get Game object
        game = Game.query.first()
        # Check if there is a ongoing round associated, if not create a new one
        if not check_if_ongoing_round(active_player):
            rnd = Round(player_id=active_player.id, ongoing=True, throwcount=0)
            db.session.add(rnd)
            db.session.commit()
        else:
            # Set round object
            rnd = Round.query.filter_by(player_id=active_player.id, ongoing=1).first()

        # set throwcount
        throwcount = rnd.throwcount

        # Check if relevant hit
        if hit in range(0, 15):
            result = "-"
        else:
            # Cricket and score
            cricket = Cricket.query.filter_by(player_id=active_player.id).first()
            # 1. Check if hit is closed already
            if not check_close(hit) == "closed":
                # get current cricket counts
                cricket_dict = dict()
                cricket_dict['15'] = cricket.c15
                cricket_dict['16'] = cricket.c16
                cricket_dict['17'] = cricket.c17
                cricket_dict['18'] = cricket.c18
                cricket_dict['19'] = cricket.c19
                cricket_dict['20'] = cricket.c20
                cricket_dict['25'] = cricket.c25
                # increase count
                cricket_dict[str(hit)] += mod
                # Write dict to database
                cricket.c15 = cricket_dict['15']
                cricket.c16 = cricket_dict['16']
                cricket.c17 = cricket_dict['17']
                cricket.c18 = cricket_dict['18']
                cricket.c19 = cricket_dict['19']
                cricket.c20 = cricket_dict['20']
                cricket.c25 = cricket_dict['25']
                db.session.commit()
                # 2. Now check if the number needs to be closed
                if not check_to_close(hit):
                    # check opened
                    if cricket_dict[str(hit)] == 3:
                        result += gettext(u" Opened!")
                # 3. Now check if it was not closed, then check scoring options
                if not check_close(hit):
                    # 4. Score
                    if check_to_score(hit, mod):
                        result += gettext(u" Scored!")
                else:
                    # If closed after last throw it returns closed
                    result += gettext(u" Closed!")
            else:
                # This happens when already closed
                result = "-"

        # Finally Check if won
        if check_won():
            game.won = True
            db.session.commit()
            result = gettext(u"Winner!")

        throwcount += 1
        rnd.throwcount = throwcount
        throw = Throw(hit=hit, mod=mod, round_id=rnd.id, player_id=active_player.id)
        if throwcount == 3:
            game.nextPlayerNeeded = True
            result += gettext(u" Remove Darts!")
        db.session.add(throw)
        db.session.commit()

        return result

    else:
        return gettext(u"There is no active game running")


def check_close(hit):
    cricket_control = CricketControl.query.first()
    cricket_dict = dict()
    cricket_dict['15'] = cricket_control.c15
    cricket_dict['16'] = cricket_control.c16
    cricket_dict['17'] = cricket_control.c17
    cricket_dict['18'] = cricket_control.c18
    cricket_dict['19'] = cricket_control.c19
    cricket_dict['20'] = cricket_control.c20
    cricket_dict['25'] = cricket_control.c25
    return str(cricket_dict[str(hit)])


def check_to_close(hit):
    close = True
    playing_players = get_playing_players_objects()
    for player in playing_players:
        cricket_dict = dict()
        cricket_object = Cricket.query.filter_by(player_id=player.id).first()
        cricket_dict['15'] = cricket_object.c15
        cricket_dict['16'] = cricket_object.c16
        cricket_dict['17'] = cricket_object.c17
        cricket_dict['18'] = cricket_object.c18
        cricket_dict['19'] = cricket_object.c19
        cricket_dict['20'] = cricket_object.c20
        cricket_dict['25'] = cricket_object.c25
        if cricket_dict[str(hit)] < 3:
            close = False
    if close:
        cricket_control_dict = dict()
        cricket_control = CricketControl.query.first()
        cricket_control_dict['15'] = cricket_control.c15
        cricket_control_dict['16'] = cricket_control.c16
        cricket_control_dict['17'] = cricket_control.c17
        cricket_control_dict['18'] = cricket_control.c18
        cricket_control_dict['19'] = cricket_control.c19
        cricket_control_dict['20'] = cricket_control.c20
        cricket_control_dict['25'] = cricket_control.c25
        cricket_control_dict[str(hit)] = "closed"
        cricket_control.c15 = cricket_control_dict['15']
        cricket_control.c16 = cricket_control_dict['16']
        cricket_control.c17 = cricket_control_dict['17']
        cricket_control.c18 = cricket_control_dict['18']
        cricket_control.c19 = cricket_control_dict['19']
        cricket_control.c20 = cricket_control_dict['20']
        cricket_control.c25 = cricket_control_dict['25']
        db.session.commit()

    return close


def check_to_score(hit, mod):
    # init scored
    scored = False
    # Get game object because we need to know variant
    game = Game.query.first()
    variant = game.variant
    # Get active Player and corresponding score (Variant: Normal)
    active_player = get_active_player()
    # Get playing Players (Variant: Cut Throat)
    playing_players = get_playing_players_objects()
    # Check if opened
    cricket_dict = dict()
    cricket_object = Cricket.query.filter_by(player_id=active_player.id).first()
    cricket_dict['15'] = cricket_object.c15
    cricket_dict['16'] = cricket_object.c16
    cricket_dict['17'] = cricket_object.c17
    cricket_dict['18'] = cricket_object.c18
    cricket_dict['19'] = cricket_object.c19
    cricket_dict['20'] = cricket_object.c20
    cricket_dict['25'] = cricket_object.c25
    if cricket_dict[str(hit)] > 3:
        if variant == "Normal":
            if not check_close(hit) == "closed":
                scored = True
                score = Score.query.filter_by(player_id=active_player.id).first()
                points = hit * mod
                score.score += points
                db.session.commit()
                return scored
        elif variant == "Cut Throat":
            if not check_close(hit) == "closed":
                # Find players which have not closed yet
                for player in playing_players:
                    cricket_dict = {}
                    cricket_object = Cricket.query.filter_by(player_id=player.id).first()
                    cricket_dict['15'] = cricket_object.c15
                    cricket_dict['16'] = cricket_object.c16
                    cricket_dict['17'] = cricket_object.c17
                    cricket_dict['18'] = cricket_object.c18
                    cricket_dict['19'] = cricket_object.c19
                    cricket_dict['20'] = cricket_object.c20
                    cricket_dict['25'] = cricket_object.c25
                    if cricket_dict[str(hit)] < 3:
                        scored = True
                        score = Score.query.filter_by(player_id=player.id).first()
                        score.score += hit * mod
                        db.session.commit()
                        return scored
    else:
        return scored


def check_won():
    all_closed = True
    won = True
    game = Game.query.first()
    playing_players = get_playing_players_objects()
    active_player = get_active_player()
    cricket = Cricket.query.filter_by(player_id=active_player.id).first()
    cricket_dict = dict()
    cricket_dict['15'] = cricket.c15
    cricket_dict['16'] = cricket.c16
    cricket_dict['17'] = cricket.c17
    cricket_dict['18'] = cricket.c18
    cricket_dict['19'] = cricket.c19
    cricket_dict['20'] = cricket.c20
    cricket_dict['25'] = cricket.c25
    for item in cricket_dict.values():
        if item < 3:
            all_closed = False
            won = False
    if all_closed:
        if game.variant == "Normal":
            for player in playing_players:
                active_score = Score.query.filter_by(player_id=active_player.id).first()
                player_score = Score.query.filter_by(player_id=player.id).first()
                if not active_player.id == player.id:
                    if active_score.score < player_score.score:
                        won = False
        elif game.variant == "Cut Throat":
            for player in playing_players:
                active_score = Score.query.filter_by(player_id=active_player.id).first()
                player_score = Score.query.filter_by(player_id=player.id).first()
                if not active_player.id == player.id:
                    if active_score.score > player_score.score:
                        won = False
        else:
            won = True
    else:
        won = False

    return won


def switch_next_player():
    # First check if the game was won
    game = Game.query.first()
    if game.won:
        return gettext(u"There is no active game running")
    else:
        # Then set active Player round ongoing to 0 and nextPlayerNeeded in Game to 0
        active_player_object = Player.query.filter_by(active=True).first()
        active_player_round = Round.query.filter_by(player_id=active_player_object.id, ongoing=1).first()
        # TODO This might to be removed again. Time will bring results
        position_list_active_player = 0
        # TODO This might to be removed again. Time will bring results
        try:
            active_player_round.ongoing = False
        except AttributeError:
            print("Error handled, lolz.")
        game.nextPlayerNeeded = False
        # Initialize variables to work with
        key = []
        list_of_playing_players = get_playing_players()
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
                    throwlist.append(str(player_id) + "," + str(last_throws[i].hit) + "," + str(last_throws[i].mod))
            except:
                print("Exception handled, lolz")
        else:
            throwlist.append(str(player_id) + ",0,0")
            throwlist.append(str(player_id) + ",0,0")
            throwlist.append(str(player_id) + ",0,0")

    return throwlist


def get_all_throws(player_id):
    throws = (Throw.query.filter_by(player_id=player_id)).all()
    return throws


def get_closed():
    cricket_control = CricketControl.query.first()
    cricket_dict = dict()
    cricket_dict['15'] = cricket_control.c15
    cricket_dict['16'] = cricket_control.c16
    cricket_dict['17'] = cricket_control.c17
    cricket_dict['18'] = cricket_control.c18
    cricket_dict['19'] = cricket_control.c19
    cricket_dict['20'] = cricket_control.c20
    cricket_dict['25'] = cricket_control.c25
    return cricket_dict