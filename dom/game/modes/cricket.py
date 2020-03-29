# Helper file for cricket

# Imports
from dom import db, socketio
from flask_babel import gettext
from dom.game.database.models import Cricket, Player, Round, Game, Podium, Throw, CricketControl, Score, PointsGained
from dom.game.common.helper import check_if_ongoing_game, check_if_ongoing_round, check_other_players, set_podium, set_last_podium, \
    get_playing_players_objects, get_active_player, get_playing_players_not_out_objects


def get_cricket(player_id):
    cricket = Cricket.query.filter_by(player_id=player_id).first()
    return cricket


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
                gained_points = PointsGained(
                    points=points, throw_id=throw_id.id + 1, player_id=player_id)
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
                        score = Score.query.filter_by(
                            player_id=player.id).first()
                        points = hit * relevant_mod
                        score.score += points
                        # Setup gained Points for updateThrow
                        throw_id = Throw.query.order_by(
                            Throw.id.desc()).first()
                        gained_points = PointsGained(
                            points=points, throw_id=throw_id.id + 1, player_id=player.id)
                        db.session.add(gained_points)
                        db.session.commit()

                return scored
    else:
        return scored


def check_won_cricket():
    all_closed = True
    won = True
    game = Game.query.first()
    active_player = get_active_player()
    cricket_dict = get_cricket_dict(active_player.id)
    players_not_out = get_playing_players_not_out_objects()
    for item in cricket_dict.values():
        if item < 3:
            all_closed = False
            won = False

    if all_closed:
        if game.variant == "Normal":
            for player in players_not_out:
                active_score = Score.query.filter_by(
                    player_id=active_player.id).first()
                player_score = Score.query.filter_by(
                    player_id=player.id).first()
                if not active_player.id == player.id:
                    if active_score.score < player_score.score:
                        won = False
        elif game.variant == "Cut Throat":
            for player in players_not_out:
                active_score = Score.query.filter_by(
                    player_id=active_player.id).first()
                player_score = Score.query.filter_by(
                    player_id=player.id).first()
                if not active_player.id == player.id:
                    if active_score.score > player_score.score:
                        won = False
        else:
            won = True
    else:
        won = False

    return won


def score_cricket(hit, mod):
    # Empty result for now
    result = ""
    audiofile = ""
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
            rnd = Round.query.filter_by(
                player_id=active_player.id, ongoing=1).first()

        # set throwcount
        throwcount = rnd.throwcount

        # Check if relevant hit
        if hit in range(0, 15):
            result = "-"
            audiofile = "beep"
        else:
            audiofile = "hit"
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
                        audiofile = "open"
                # 3. Now check if it was not closed, then check scoring options
                if not check_close(hit):
                    if cricket_dict[str(hit)] > 3:
                        if check_to_score(hit, mod, hit_before_increase, active_player.id):
                            result += gettext(u" Scored!")
                            audiofile = "score"
                else:
                    result += gettext(u" Closed!")
                    audiofile = "close"
            else:
                # This happens when already closed
                cricket_dict = get_cricket_dict(active_player.id)
                cricket_dict[str(hit)] += mod
                set_cricket_dict(active_player.id, cricket_dict)
                result = "-"
                audiofile = "beep"

        # Finally Check if Player is out
        if check_won_cricket():
            # Check if there are other players left to play
            if check_other_players() > 2:
                # Wording
                if Podium.query.first():
                    result = gettext(u" Next Winner")
                else:
                    result = gettext(u"Winner!")
                # Do Podium Things
                set_podium(active_player.id)
                db.session.commit()
            else:
                # Game is over
                set_podium(active_player.id)
                set_last_podium()
                game.won = True
                db.session.commit()
                result += gettext(u" Game Over!")

        # Do final round handling
        throwcount += 1
        rnd.throwcount = throwcount
        throw = Throw(hit=hit, mod=mod, round_id=rnd.id,
                      player_id=active_player.id)
        if throwcount == 3:
            game.nextPlayerNeeded = True
            result += gettext(u" Remove Darts!")
        db.session.add(throw)
        db.session.commit()

        return result, audiofile

    else:
        return gettext(u"There is no active game running")


def update_throw_table(throw_id, hit, mod):
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
            db.session.query(PointsGained).filter(
                PointsGained.id == gp.id).delete()
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
            check_to_score(int(hit), int(
                mod), hit_before_increase, throw.player_id)

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
