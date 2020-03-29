# Helper file for Split-Score

# Imports
from dom import db
from flask_babel import gettext
from dom.game.database.models import Score, Game, Round, Throw, Split, Player, PointsGained
from dom.game.common.helper import check_if_ongoing_game, get_active_player, check_if_ongoing_round, get_playing_players_id, \
    update_throw_and_score


def score_split(hit, mod):
    # check if there is a game going on
    if check_if_ongoing_game():
        # Set split false
        split = False
        scored = False
        # Get active player
        active_player = get_active_player()
        # Get players number to hit
        split_object = Split.query.filter_by(
            player_id=active_player.id).first()
        # Get game variant
        game = Game.query.first()
        # Calculate point which might be gained
        points = int(hit) * int(mod)
        # Check if there is a ongoing round associated, if not create a new one
        if not check_if_ongoing_round(active_player):
            rnd = Round(player_id=active_player.id, ongoing=True, throwcount=0)
            score = Score.query.filter_by(player_id=active_player.id).first()
            score.parkScore = score.score
            db.session.add(rnd)
            db.session.commit()
        else:
            # Set round object
            rnd = Round.query.filter_by(
                player_id=active_player.id, ongoing=1).first()
        # Check if ongoing round is over
        if rnd.throwcount == 3:
            game.nextPlayerNeeded = True
        else:
            # Determine throwcount
            throwcount = rnd.throwcount
            # Get player rounds
            rnds = Round.query.filter_by(player_id=active_player.id).all()
            # Check if it is steeldart variant and if there is score to be gained
            if game.variant == "steeldart":
                # Check if there is only one round associated with the player
                if len(rnds) == 1:
                    # Add Throw to Score
                    add_score(active_player.id, points)
                    result = "-"
                else:
                    result, split, scored = check_to_score(split_object.next_hit, hit, mod,
                                                           points, active_player.id, throwcount)

            else:
                result, split, scored = check_to_score(split_object.next_hit, hit, mod, points, active_player.id,
                                                       throwcount)

            # Increase throwcount and so on
            throwcount += 1
            rnd.throwcount = throwcount
            throw = Throw(hit=hit, mod=mod, round_id=rnd.id,
                          player_id=active_player.id)
            if throwcount == 3:
                game.nextPlayerNeeded = True
                split_object.has_been_hit = False
                if game.variant == "steeldart":
                    if not len(Round.query.filter_by(player_id=active_player.id).all()) == 1:
                        nexthit = proceed_to_next_hit(split_object.next_hit)
                        split_object.next_hit = nexthit
                else:
                    nexthit = proceed_to_next_hit(split_object.next_hit)
                    split_object.next_hit = nexthit

                db.session.commit()

                if split:
                    result = gettext(u"Split Score! Remove Darts!")
                else:
                    result = gettext(u"Remove Darts!")

            db.session.add(throw)
            db.session.commit()

            # If points were gained add them for reverting possibility
            if scored:
                throwid = Throw.query.order_by(Throw.id.desc()).first()
                add_points_gained(points, throwid.id, active_player.id)

            if check_end_game():
                game.won = True
                db.session.commit()
                result = gettext(u"Game Over!")

            return result


def add_score(player_id, points):
    # Get player current score
    score = Score.query.filter_by(player_id=player_id).first()
    newscore = score.score + points
    score.score = newscore


def add_points_gained(points, throwid, playerid):
    # Setup gained Points for updateThrow
    gained_points = PointsGained(
        points=points, throw_id=throwid, player_id=playerid)
    db.session.add(gained_points)
    db.session.commit()


def split_score(player_id):
    # Get player current score
    score = Score.query.filter_by(player_id=player_id).first()
    newscore = round(score.score / 2)
    score.score = newscore
    db.session.commit()


def unsplit_score(player_id):
    # Return to park score
    score = Score.query.filter_by(player_id=player_id).first()
    score.score = score.parkScore
    db.session.commit()


def check_to_score(nexthit, hit, mod, points, playerid, throwcount):
    result = "-"
    split = False
    scored = False
    # If hit is next hit count to score
    if nexthit == "double":
        if mod == 2:
            add_score(playerid, points)
            set_has_been_hit(playerid, True)
            scored = True
            result = gettext(u"Scored")
        else:
            if throwcount == 2:
                if not get_has_been_hit(playerid):
                    split_score(playerid)
                    split = True
    elif nexthit == "triple":
        if mod == 3:
            add_score(playerid, points)
            set_has_been_hit(playerid, True)
            scored = True
            result = gettext(u"Scored")
        else:
            if throwcount == 2:
                if not get_has_been_hit(playerid):
                    split_score(playerid)
                    split = True
    elif nexthit == "Bulls":
        if hit == 25:
            add_score(playerid, points)
            set_has_been_hit(playerid, True)
            scored = True
            result = gettext(u"Scored")
        else:
            if throwcount == 2:
                if not get_has_been_hit(playerid):
                    split_score(playerid)
                    split = True
    else:
        if str(hit) == nexthit:
            add_score(playerid, points)
            set_has_been_hit(playerid, True)
            scored = True
            result = gettext(u"Scored")
        # Else if not hit and round is over divide score
        else:
            if throwcount == 2:
                if not get_has_been_hit(playerid):
                    split_score(playerid)
                    split = True

    return result, split, scored


def proceed_to_next_hit(nexthit):
    if nexthit == "16":
        nexthit = "double"
    elif nexthit == "18":
        nexthit = "triple"
    elif nexthit == "double":
        nexthit = "17"
    elif nexthit == "triple":
        nexthit = "19"
    elif nexthit == "20":
        nexthit = "Bulls"
    elif nexthit == "Bulls":
        nexthit = "-"
    else:
        next_string = int(nexthit) + 1
        nexthit = str(next_string)

    return nexthit


def check_end_game():
    game_ended = True
    # Check if everyones next hit number is -
    playing_players = get_playing_players_id()
    for player_id in playing_players:
        if Split.query.filter_by(player_id=player_id).first().next_hit != "-":
            game_ended = False
    return game_ended


def set_has_been_hit(player_id, value):
    split = Split.query.filter_by(player_id=player_id).first()
    split.has_been_hit = value
    db.session.commit()


def get_has_been_hit(player_id):
    split = Split.query.filter_by(player_id=player_id).first()
    return split.has_been_hit


def build_podium():
    scores = Score.query.order_by(Score.score.desc()).all()
    player_podium = []
    place = 1
    for score in scores:
        player_podium.append(str(Player.query.filter_by(
            id=score.player_id).first().name) + "," + str(place))
        place += 1

    return player_podium


def format_to_split(hit, mod, next_hit):
    if hit == 25:
        output = "Bulls"
    elif next_hit == "double":
        if str(mod) == "2":
            output = "double"
        else:
            output = str(hit)
    elif next_hit == "triple":
        if str(mod) == "3":
            output = "triple"
        else:
            output = str(hit)
    else:
        output = str(hit)

    return output


def update_throw_table(throwid, hit, mod):
    # Get the throw to change
    throw = Throw.query.filter_by(id=throwid).first()
    # Get nextHit of this throw
    split = Split.query.filter_by(player_id=throw.player_id).first()
    # Get player Round
    rnd = Round.query.filter_by(
        player_id=throw.player_id).order_by(Round.id.desc()).first()
    # Get player score
    score = Score.query.filter_by(player_id=throw.player_id).first()
    # Get game for game variant
    game = Game.query.first()
    # Get player rounds
    rnds = Round.query.filter_by(player_id=throw.player_id).all()

    # Now handle steel dart variant first round throw change
    if game.variant == "steeldart":
        # Check if there is only one round associated with the player
        if len(rnds) == 1:
            # Just edit score
            update_throw_and_score(throw, hit, mod, True)

        else:
            # It is a mid game throw update, so do throw update routine
            update_throw_routine(rnd, split, throw, hit, mod, score)

    else:
        # E-Dart Variant - Do throw update routine
        update_throw_routine(rnd, split, throw, hit, mod, score)


def update_throw_routine(rnd, split, throw, hit, mod, score):
    # Now lets determine which was the number which should have been hit depending on throwcount
    if rnd.throwcount == 3:
        if split.next_hit == "double":
            next_hit = "16"
        elif split.next_hit == "17":
            next_hit = "double"
        elif split.next_hit == "19":
            next_hit = "triple"
        elif split.next_hit == "triple":
            next_hit = "18"
        elif split.next_hit == "Bulls":
            next_hit = "20"
        elif split.next_hit == "-":
            next_hit = "Bulls"
        else:
            next_hit = str(int(split.next_hit) - 1)
    else:
        next_hit = str(split.next_hit)

    # Next up format old hit to split language
    oldhit = format_to_split(throw.hit, throw.mod, next_hit)

    # Format new hit
    newhit = format_to_split(hit, mod, next_hit)

    # Undo any gained points first
    points_gained = PointsGained.query.filter_by(throw_id=throw.id).first()
    if points_gained:
        score.score -= points_gained.points
        db.session.query(PointsGained).filter(
            PointsGained.id == points_gained.id).delete()
        db.session.commit()

    # Then change the throw in database
    throw.hit = int(hit)
    throw.mod = int(mod)
    db.session.commit()

    # Next up check if the change is relevant
    if (oldhit == next_hit) or (newhit == next_hit):
        # Determine if the score has to be split or doubled up again
        # get all throws associated to round
        throws = Throw.query.filter_by(round_id=rnd.id).all()
        if len(throws) == 3:
            # First check if score was splitted
            if score.score > score.parkScore:
                splitted = False
            elif score.score == score.parkScore:
                splitted = False
            else:
                splitted = True

            # Now if score was splitted before check if it needs to be unsplitted now
            if splitted:
                unsplit = False
                for tr in throws:
                    check_hit = format_to_split(tr.hit, tr.mod, next_hit)
                    if check_hit == next_hit:
                        unsplit = True
                if unsplit:
                    unsplit_score(throw.player_id)

            # Now check if it needs to be splitted otherwise
            if not splitted:
                to_split = True
                for tr in throws:
                    check_hit = format_to_split(tr.hit, tr.mod, next_hit)
                    if check_hit == next_hit:
                        to_split = False
                if to_split:
                    split_score(throw.player_id)

        # now we need to determine if the change might gain new points
        if newhit == next_hit:
            # New Points are gained
            points = int(hit) * int(mod)
            add_score(player_id=throw.player_id, points=points)
            set_has_been_hit(throw.player_id, True)
            add_points_gained(points, throw.id, throw.player_id)
