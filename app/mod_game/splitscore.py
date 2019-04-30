# Helper file for Split-Score

# Imports
from app import db, socketio
from flask_babel import gettext
from .models import Score, Game, Round, Throw, Split, Player
from .helper import check_if_ongoing_game, get_active_player, check_if_ongoing_round, get_playing_players_id


def score_split(hit, mod):
    # check if there is a game going on
    if check_if_ongoing_game():
        # Set split false
        split = False
        # Get active player
        active_player = get_active_player()
        # Get players number to hit
        split_object = Split.query.filter_by(player_id=active_player.id).first()
        # Get game variant
        game = Game.query.first()
        # Calculate point which might be gained
        points = int(hit) * int(mod)
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
                    result, split = check_to_score(split_object.next_hit, hit, mod, points, active_player.id, throwcount)

            else:
                result, split = check_to_score(split_object.next_hit, hit, mod, points, active_player.id, throwcount)

            # Increase throwcount and so on
            throwcount += 1
            rnd.throwcount = throwcount
            throw = Throw(hit=hit, mod=mod, round_id=rnd.id, player_id=active_player.id)
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
    db.session.commit()


def split_score(player_id):
    # Get player current score
    score = Score.query.filter_by(player_id=player_id).first()
    newscore = round(score.score / 2)
    score.score = newscore
    db.session.commit()


def check_to_score(nexthit, hit, mod, points, playerid, throwcount):
    result = "-"
    split = False
    # If hit is next hit count to score
    if nexthit == "double":
        if mod == 2:
            add_score(playerid, points)
            set_has_been_hit(playerid, True)
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
            result = gettext(u"Scored")
        # Else if not hit and round is over divide score
        else:
            if throwcount == 2:
                if not get_has_been_hit(playerid):
                    split_score(playerid)
                    split = True

    return result, split


def proceed_to_next_hit(nexthit):
    if nexthit == "16":
        nexthit = "double"
    elif nexthit == "18":
        nexthit = "triple"
    elif nexthit == "double":
        nexthit = "17"
    elif nexthit == "triple":
        nexthit = "19"
    else:
        next_string = int(nexthit) + 1
        nexthit = str(next_string)

    return nexthit


def check_end_game():
    game_ended = True
    # Check if everyones next hit number is 21
    playing_players = get_playing_players_id()
    for player_id in playing_players:
        if Split.query.filter_by(player_id=player_id).first().next_hit != "21":
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
        player_podium.append(str(Player.query.filter_by(id=score.player_id).first().name) + "," + str(place))
        place += 1

    return player_podium


def update_throw_table(throwid, hit, mode):
    pass
