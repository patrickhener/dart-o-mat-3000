# helper file for X01

# imports
from dom import db
from flask_babel import gettext
from dom.game.database.models import Score, Game, Player, Round, Podium, Throw
from dom.game.common.helper import check_if_ongoing_game, check_if_ongoing_round, check_other_players, set_podium, set_last_podium, \
    update_throw_and_score
from dom.game.common.dictionaries import double_checkout_dict, master_checkout_dict


def get_checkout(score):
    if score < 171:
        # TODO implement double/master check here later
        if str(score) in double_checkout_dict:
            checkout = double_checkout_dict[str(score)]
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
            rnd = Round.query.filter_by(
                player_id=active_player.id, ongoing=1).first()

        # Check if ongoing round is over
        if rnd.throwcount == 3:
            game.nextPlayerNeeded = True
        else:
            # set throwcount and old score
            throwcount = rnd.throwcount
            player_score = Score.query.filter_by(
                player_id=active_player.id).first()
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
                    throw = Throw(hit=hit, mod=mod, round_id=rnd.id,
                                  player_id=active_player.id)
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
    update_throw_and_score(throw, hit, mod, False)
