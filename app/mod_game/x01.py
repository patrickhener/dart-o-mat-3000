# helper file for X01

# imports
from app import db
from flask_babel import gettext
from .models import Score, Game, Player, Round, Podium, Throw
from .helper import check_if_ongoing_game, check_if_ongoing_round, check_other_players, set_podium, set_last_podium

# Dictionaries
checkout_dict = {
    "170": "T20 T20 Bull",
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


def get_checkout(score):
    if score < 171:
        if str(score) in checkout_dict:
            checkout = checkout_dict[str(score)]
            return checkout
        else:
            return "-"
    else:
        return "-"


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
    if not (game.outGame == gettext("Straight")):
        if new_score == 1:
            return False
        else:
            return True
    else:
        return True


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
                    # Check if there are other players left to play
                    if check_other_players() > 2:
                        # Check for wording
                        # If there is already a first place wording is different
                        # First Place will be gettext(u"Winner!")
                        # Every other placement will be something else
                        if Podium.query.first():
                            result = gettext(u"Next Winner")
                        else:
                            result = gettext(u"Winner!")
                        # Do Podium Things
                        set_podium(active_player.id)
                        throwcount += 1
                        rnd.throwcount = throwcount
                        player_score.score = 0
                        db.session.commit()

                        return result
                    else:
                        set_podium(active_player.id)
                        set_last_podium()
                        game.won = True
                        throwcount += 1
                        rnd.throwcount = throwcount
                        player_score.score = 0
                        db.session.commit()
                        # Check wording for games with just two players
                        if len(Player.query.filter_by(game_id=1).all()) == 2:
                            return gettext(u"Winner!")
                        else:
                            return gettext(u"Game Over!")
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


def update_throw_table(throw_id, hit, mod):
    # get Throw and score
    throw = Throw.query.filter_by(id=throw_id).first()
    score = Score.query.filter_by(player_id=throw.player_id).first()
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
