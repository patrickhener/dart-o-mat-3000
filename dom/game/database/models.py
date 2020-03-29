# Import the database object (db) from the main application module
from dom import db


# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


# Define game related models
class Game(Base):
    gametype = db.Column(db.String, nullable=False)
    inGame = db.Column(db.String)
    outGame = db.Column(db.String)
    variant = db.Column(db.String)
    won = db.Column(db.Boolean, default=False)
    nextPlayerNeeded = db.Column(db.Boolean, default=False)

    players = db.relationship('Player', backref='players', lazy=True)

    def __repr__(self):
        return self.gametype


class Player(Base):
    name = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean)
    out = db.Column(db.Boolean)

    rounds = db.relationship('Round', backref='rounds', lazy=True)
    throws = db.relationship('Throw', backref='throws', lazy=True)
    scores = db.relationship('Score', backref='scores', lazy=True)
    crickets = db.relationship('Cricket', backref='crickets', lazy=True)
    gained = db.relationship('PointsGained', backref='playergaines', lazy=True)
    numbers = db.relationship('ATC', backref='numbers', lazy=True)
    nexthits = db.relationship('Split', backref='nexthits', lazy=True)
    podiums = db.relationship('Podium', backref='podiums', lazy=True)

    game_id = db.Column(db.Integer, db.ForeignKey(
        'game.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)

    def __repr__(self):
        return self.name


class Score(Base):
    score = db.Column(db.Integer, nullable=False)
    parkScore = db.Column(db.Integer, nullable=False)
    initialScore = db.Column(db.Integer, nullable=False)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"),
                          nullable=False)

    def __int__(self):
        return self.count


class Cricket(Base):
    c20 = db.Column(db.Integer, nullable=True)
    c19 = db.Column(db.Integer, nullable=True)
    c18 = db.Column(db.Integer, nullable=True)
    c17 = db.Column(db.Integer, nullable=True)
    c16 = db.Column(db.Integer, nullable=True)
    c15 = db.Column(db.Integer, nullable=True)
    c25 = db.Column(db.Integer, nullable=True)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"),
                          nullable=False)

    def __repr__(self):
        return str(self.id)


class CricketControl(Base):
    c20 = db.Column(db.String, nullable=True)
    c19 = db.Column(db.String, nullable=True)
    c18 = db.Column(db.String, nullable=True)
    c17 = db.Column(db.String, nullable=True)
    c16 = db.Column(db.String, nullable=True)
    c15 = db.Column(db.String, nullable=True)
    c25 = db.Column(db.String, nullable=True)

    def __repr__(self):
        return str(self.id)


class PointsGained(Base):
    points = db.Column(db.Integer, nullable=False)

    throw_id = db.Column(db.Integer, db.ForeignKey(
        'throw.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey(
        'player.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return str(self.id)


class Round(Base):
    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"),
                          nullable=False)
    ongoing = db.Column(db.Boolean, nullable=False)
    throwcount = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return self.id


class Throw(Base):
    hit = db.Column(db.Integer, nullable=False)
    mod = db.Column(db.Integer, nullable=False)

    gained = db.relationship('PointsGained', backref='throwgaines', lazy=True)

    round_id = db.Column(db.Integer, db.ForeignKey(
        'round.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"),
                          nullable=False)

    def __repr__(self):
        hitcount = self.hit * self.mod
        return str(hitcount)


class ATC(Base):
    number = db.Column(db.Integer, nullable=True)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"),
                          nullable=False)

    def __repr__(self):
        return str(self.number)


class Podium(Base):
    place = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"),
                          nullable=False)

    def __repr__(self):
        return str(self.place)


class Split(Base):
    next_hit = db.Column(db.String, nullable=False)
    has_been_hit = db.Column(db.Boolean, nullable=False)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"),
                          nullable=False)

    def __repr__(self):
        return self.next_hit
