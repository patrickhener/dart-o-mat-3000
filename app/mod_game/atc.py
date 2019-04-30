# Helper file for Around the clock

# Imports
from app import db
from flask_babel import gettext
from .models import ATC, Game, Round, Podium, Throw
from .helper import check_if_ongoing_game, get_active_player, check_if_ongoing_round, check_other_players, set_podium, \
    set_last_podium


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
                    # Player won, now check podium things
                    # If there are still more than 2 not out player do Podium things
                    if check_other_players() > 2:
                        # Do Podium Things
                        # Check wording for result
                        if Podium.query.first():
                            result = gettext(u"Next Winner")
                        else:
                            result = gettext(u"Winner!")
                        set_podium(active_player.id)
                        number_to_hit.number = 0
                    # Else Game is over
                    else:
                        set_podium(active_player.id)
                        set_last_podium()
                        number_to_hit.number = 0
                        game.won = True
                        result = gettext(u"Game Over!")
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


def update_throw_table(throw_id, hit, mod):
    # get Game
    game = Game.query.first()
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
