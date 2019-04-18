# Import db from app
from app import db, socketio
# Import module models
from app.mod_game.models import Game, Player, Score, Cricket, Round, Throw, CricketControl, PointsGained, ATC
# cycle and islice for nextPlayer
from itertools import cycle, islice
# Babel Translation
from flask_babel import gettext


# Dictionaries
checkout_dict = {
    "170": "T0 T20 Bull",
    "167": "T20 T19 Bull",
    "164": "T19 T19 Bull",
    "161": "T20 T17 Bull",
    "160": "T20 T20 D20",
    "158": "T20 T20 D19",
    "157": "T19 T20 D20",
    "156": "T20 T20 D18",
    "155": "T20 T19 D19",
    "154": "T20 T18 D20",
    "153": "T20 T19 D18",
    "152": "T20 T20 D16",
    "151": "T20 T17 D20",
    "150": "T20 T18 D18",
    "149": "T20 T19 D16",
    "148": "T20 T20 D14",
    "147": "T20 T17 D18",
    "146": "T20 T18 D16",
    "145": "T20 T15 D20",
    "144": "T20 T20 D12",
    "143": "T20 T17 D16",
    "142": "T20 T14 D20",
    "141": "T20 T15 D18",
    "140": "T20 T16 D16",
    "139": "T20 T13 D20",
    "138": "T20 T16 D15",
    "137": "T18 T17 D16",
    "136": "T20 T20 D8",
    "135": "T20 T13 D18",
    "134": "T20 T14 D16",
    "133": "T20 T19 D8",
    "132": "T20 T16 D12",
    "131": "T20 T13 D16",
    "130": "T20 T18 D8",
    "129": "T19 T16 D12",
    "128": "T20 T20 D4",
    "127": "T20 T17 D8",
    "126": "T19 19 Bull",
    "125": "T20 T19 D4",
    "124": "T20 T16 D8",
    "123": "T20 T13 D12",
    "122": "T18 18 Bull",
    "121": "T19 14 Bull",
    "120": "T20 20 D20",
    "119": "T20 19 D20",
    "118": "T20 18 D20",
    "117": "T20 17 D20",
    "116": "T20 16 D20",
    "115": "T20 15 D20",
    "114": "T20 14 D20",
    "113": "T20 13 D20",
    "112": "T20 12 D20",
    "111": "T20 19 D16",
    "110": "T20 10 D20",
    "109": "T19 12 D20",
    "108": "T20 16 D16",
    "107": "T19 10 D20",
    "106": "T20 10 D18",
    "105": "T20 13 D16",
    "104": "T20 12 D16",
    "103": "T19 10 D18",
    "102": "T20 10 D16",
    "101": "T17 10 D20",
    "100": "T20 D20",
    "99": "T19 10 D16",
    "98": "T20 D19",
    "97": "T19 D20",
    "96": "T20 D18",
    "95": "T19 D19",
    "94": "T18 D20",
    "93": "T19 D18",
    "92": "T20 D16",
    "91": "T17 D20",
    "90": "T18 D18",
    "89": "T19 D16",
    "88": "T16 D20",
    "87": "T17 D18",
    "86": "T18 D16",
    "85": "T15 D20",
    "84": "T16 D18",
    "83": "T17 D16",
    "82": "T14 D20",
    "81": "T15 D18",
    "80": "T16 D16",
    "79": "T13 D20",
    "78": "T18 D12",
    "77": "T15 D16",
    "76": "T20 D8",
    "75": "T13 D18",
    "74": "T14 D16",
    "73": "T19 D8",
    "72": "T16 D12",
    "71": "T13 D16",
    "70": "T18 D8",
    "69": "19 Bull",
    "68": "T20 D4",
    "67": "T17 D8",
    "66": "T10 D18",
    "65": "T19 D4",
    "64": "T16 D8",
    "63": "T13 D12",
    "62": "T10 D16",
    "61": "T15 D8",
    "60": "20 D20",
    "59": "19 D20",
    "58": "18 D20",
    "57": "17 D20",
    "56": "16 D20",
    "55": "15 D20",
    "54": "14 D20",
    "53": "13 D20",
    "52": "12 D20",
    "51": "19 D16",
    "50": "10 D20",
    "49": "17 D16",
    "48": "16 D16",
    "47": "15 D16",
    "46": "6 D20",
    "45": "13 D16",
    "44": "12 D16",
    "43": "3 D20",
    "42": "10 D16",
    "41": "9 D16",
    "40": "D20"
}


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

    playing_players_object = Player.query.filter_by(game_id=1).all()
    for player in playing_players_object:
        player.game_id = None
        player.active = 0

    db.session.commit()


def get_checkout(score):
    if score < 171:
        if str(score) in checkout_dict:
            checkout = checkout_dict[str(score)]
            return checkout
        else:
            return "-"
    else:
        return "-"


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
        # get throw to change
        throw = Throw.query.filter_by(id=throw_id).first()
        # Case Switching
        # Case 0: change from 0-14 to 0-14 which is irrelevant change, just updates
        # Case 1: change from 0-14 to 15 and up, new points may be gained
        # Case 2: change from 15 and up to another 15 and up, new points may be gained
        # Case 3: change from 15 and up to below 15, just remove points and correct throw
        #         no new points can be gained
        #
        # CASE 0: Check if throw is irrelevant for score and tracking changes
        if (throw.hit < 15) and (int(hit) < 15):
            # CASE 0: Just update Throw in table
            throw.hit = int(hit)
            throw.mod = int(mod)
            db.session.commit()
        else:
            # First undo all changes made by throw
            # get gained Points from throwid
            gained_points = PointsGained.query.filter_by(throw_id=throw_id).all()
            # for each player which has gained points reduce score again
            for gp in gained_points:
                # Find corresponding user
                player_id = gp.player_id
                # get his score
                score = Score.query.filter_by(player_id=player_id).first()
                # reduce score again
                score.score -= gp.points
                # remove points gained entry
                db.session.query(PointsGained).filter(PointsGained.id == gp.id).delete()
                db.session.commit()

            # CASE 1-3: Correct Throw count
            # Find cricket array for player and update count
            if throw.hit > 14:
                cricket_dict = get_cricket_dict(throw.player_id)
                cricket_dict[str(throw.hit)] -= int(throw.mod)
                set_cricket_dict(throw.player_id, cricket_dict)

            # 3. look if something has to be reopened again
            # get status of CricketControl on number
            if throw.hit > 14:
                cricket_control_dict = get_cricket_control()
                closed_status = cricket_control_dict[str(throw.hit)]

                # if closed check to close
                if closed_status == "closed":
                    if not check_to_close(throw.hit):
                        # reopen in cricket control
                        cricket_control_dict[str(throw.hit)] = ""
                        set_cricket_control(cricket_control_dict)

            # Commit to db
            throw.hit = int(hit)
            throw.mod = int(mod)
            db.session.commit()

            # Now look if the new throw might gain points or close something
            # CASE 1 + 2: gain new points?
            if int(hit) > 14:
                # First book in the new hit to cricket_dict
                cricket_dict = get_cricket_dict(throw.player_id)
                hit_before_increase = cricket_dict[str(hit)]
                cricket_dict[str(hit)] += int(mod)
                set_cricket_dict(throw.player_id, cricket_dict)
                # 3. look if there are new points
                check_to_score(int(hit), int(mod), hit_before_increase, throw.player_id)

                # now check if the corrected throw might close something
                cricket_control_dict = get_cricket_control()
                closed_status = cricket_control_dict[str(hit)]

                # if not closed -> check to close
                if not closed_status == "closed":
                    check_to_close(hit)

                # Commit to db
                throw.hit = int(hit)
                throw.mod = int(mod)
                db.session.commit()

            # Redraw scoreboard after change
            socketio.emit('redrawCricket', gettext(u"Throw updated"))

    # This handles X01 games
    elif "01" in game.gametype:
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
        throw.mod = int(mod)
        # Set Score and Park Score to new Score
        score.score = new_score
        score.parkScore = new_score
        # Commit to db
        db.session.commit()

    # This handles Around the Clock games
    elif game.gametype == "ATC":
        # get Throw
        throw = Throw.query.filter_by(id=throw_id).first()
        # decrease the number again
        number = ATC.query.filter_by(player_id=throw.player_id).first()
        if game.variant == "Normal":
            number.number -= 1
        else:
            number.number -= throw.mod
        # Set Throw to new values
        throw.hit = int(hit)
        throw.mod = int(mod)
        # Commit to DB
        db.session.commit()

    # This handles any other gametype for now.
    else:
        pass

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
            # 1. Check if hit is closed already
            if not check_close(hit) == "closed":
                # get current cricket counts and increase count
                cricket_dict = get_cricket_dict(active_player.id)
                # Number has been hit before how many times?
                hit_before_increase = cricket_dict[str(hit)]
                # Now increase
                cricket_dict[str(hit)] += mod
                set_cricket_dict(active_player.id, cricket_dict)
                # 2. Now check if the number needs to be closed
                if not check_to_close(hit):
                    # check opened
                    if cricket_dict[str(hit)] == 3:
                        result += gettext(u" Opened!")
                # 3. Now check if it was not closed, then check scoring options
                if not check_close(hit):
                    if cricket_dict[str(hit)] > 3:
                        if check_to_score(hit, mod, hit_before_increase, active_player.id):
                            result += gettext(u" Scored!")
                else:
                    result += gettext(u" Closed!")
            else:
                # This happens when already closed
                cricket_dict = get_cricket_dict(active_player.id)
                cricket_dict[str(hit)] += mod
                set_cricket_dict(active_player.id, cricket_dict)
                result = "-"

        # Finally Check if won
        if check_won():
            game.won = True
            db.session.commit()
            result = gettext(u"Winner!")

        # Do final round handling
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


def score_atc(hit, mod):
    # check if there is a game going on
    if check_if_ongoing_game():
        # Get active player
        active_player = get_active_player()
        # Get players number to hit
        number_to_hit = ATC.query.filter_by(player_id=active_player.id).first()
        # Get game variant
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
            # Score
            if number_to_hit.number == int(hit):
                if game.variant == "Normal":
                    number_to_hit.number += 1
                else:
                    number_to_hit.number += mod

                # Check won
                if number_to_hit.number > 20:
                    number_to_hit.number = 0
                    game.won = True
                    result = gettext(u"Winner!")
                else:
                    result = gettext(u"Hit")

                throwcount += 1
                rnd.throwcount = throwcount
                throw = Throw(hit=hit, mod=mod, round_id=rnd.id, player_id=active_player.id)
                if throwcount == 3:
                    game.nextPlayerNeeded = True
                    result = gettext(u"Remove Darts!")
                db.session.add(throw)
                db.session.commit()
                return result
            else:
                result = "-"
                throwcount += 1
                rnd.throwcount = throwcount
                throw = Throw(hit=hit, mod=mod, round_id=rnd.id, player_id=active_player.id)
                if throwcount == 3:
                    game.nextPlayerNeeded = True
                    result = gettext(u"Remove Darts!")
                db.session.add(throw)
                db.session.commit()
                return result
    else:
        # Output if no game is running
        return gettext("There is no active game running")


def get_cricket_dict(player_id):
    cricket = Cricket.query.filter_by(player_id=player_id).first()
    cricket_dict = dict()
    cricket_dict['15'] = cricket.c15
    cricket_dict['16'] = cricket.c16
    cricket_dict['17'] = cricket.c17
    cricket_dict['18'] = cricket.c18
    cricket_dict['19'] = cricket.c19
    cricket_dict['20'] = cricket.c20
    cricket_dict['25'] = cricket.c25
    return cricket_dict


def set_cricket_dict(player_id, cricket_dict):
    cricket = Cricket.query.filter_by(player_id=player_id).first()
    cricket.c15 = cricket_dict['15']
    cricket.c16 = cricket_dict['16']
    cricket.c17 = cricket_dict['17']
    cricket.c18 = cricket_dict['18']
    cricket.c19 = cricket_dict['19']
    cricket.c20 = cricket_dict['20']
    cricket.c25 = cricket_dict['25']
    db.session.commit()
    return "Done"


def get_cricket_control():
    cricket_control = CricketControl.query.first()
    cricket_control_dict = dict()
    cricket_control_dict['15'] = cricket_control.c15
    cricket_control_dict['16'] = cricket_control.c16
    cricket_control_dict['17'] = cricket_control.c17
    cricket_control_dict['18'] = cricket_control.c18
    cricket_control_dict['19'] = cricket_control.c19
    cricket_control_dict['20'] = cricket_control.c20
    cricket_control_dict['25'] = cricket_control.c25
    return cricket_control_dict


def set_cricket_control(cricket_control_dict):
    cricket_control = CricketControl.query.first()
    cricket_control.c15 = cricket_control_dict['15']
    cricket_control.c16 = cricket_control_dict['16']
    cricket_control.c17 = cricket_control_dict['17']
    cricket_control.c18 = cricket_control_dict['18']
    cricket_control.c19 = cricket_control_dict['19']
    cricket_control.c20 = cricket_control_dict['20']
    cricket_control.c25 = cricket_control_dict['25']
    db.session.commit()
    return "Done"


def check_close(hit):
    cricket_control_dict = get_cricket_control()
    return str(cricket_control_dict[str(hit)])


def check_to_close(hit):
    close = True
    playing_players = get_playing_players_objects()
    for player in playing_players:
        cricket_dict = get_cricket_dict(player.id)
        if cricket_dict[str(hit)] < 3:
            close = False
    if close:
        cricket_control_dict = get_cricket_control()
        cricket_control_dict[str(hit)] = "closed"
        set_cricket_control(cricket_control_dict)

    return close


def check_to_score(hit, mod, hit_before, player_id):
    # init scored
    scored = False
    # Get game object because we need to know variant
    game = Game.query.first()
    variant = game.variant
    # Get playing Players (Variant: Cut Throat)
    playing_players = get_playing_players_objects()
    # Check if opened
    cricket_dict = get_cricket_dict(player_id=player_id)
    if cricket_dict[str(hit)] > 3:
        # Calculate relevant mod agains hit before count
        already_hit_subsctraction = 3 - hit_before
        if already_hit_subsctraction < 0:
            already_hit_subsctraction = 0
        relevant_mod = mod - already_hit_subsctraction
        # Actual scoring
        if variant == "Normal":
            if not check_close(hit) == "closed":
                # Scoring
                scored = True
                score = Score.query.filter_by(player_id=player_id).first()
                # check out last cricket dict number
                points = hit * relevant_mod
                score.score += points
                # Setup gained Points for updateThrow
                throw_id = Throw.query.order_by(Throw.id.desc()).first()
                gained_points = PointsGained(points=points, throw_id=throw_id.id+1, player_id=player_id)
                db.session.add(gained_points)
                db.session.commit()
                return scored
        elif variant == "Cut Throat":
            if not check_close(hit) == "closed":
                # Find players which have not closed yet
                for player in playing_players:
                    cricket_dict = get_cricket_dict(player.id)
                    if cricket_dict[str(hit)] < 3:
                        # Scoring
                        scored = True
                        score = Score.query.filter_by(player_id=player.id).first()
                        points = hit * relevant_mod
                        score.score += points
                        # Setup gained Points for updateThrow
                        throw_id = Throw.query.order_by(Throw.id.desc()).first()
                        gained_points = PointsGained(points=points, throw_id=throw_id.id+1, player_id=player.id)
                        db.session.add(gained_points)
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
    cricket_dict = get_cricket_dict(active_player.id)
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
                    throwlist.append(str(player_id) + "," + str(last_throws[i].id) + "," + str(last_throws[i].hit)
                                     + "," + str(last_throws[i].mod))
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