# Import the database object (db) from the main application module
from app import db

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

    rounds = db.relationship('Round', backref='rounds', lazy=True)
    throws = db.relationship('Throw', backref='throws', lazy=True)
    lastthrows = db.relationship('LastThrows', backref='lastthrows', lazy=True)
    scores = db.relationship('Score', backref='scores', lazy=True)
    crickets = db.relationship('Cricket', backref='crickets', lazy=True)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)

    def __repr__(self):
        return self.name

class Score(Base):
    score = db.Column(db.Integer, nullable=False)
    parkScore = db.Column(db.Integer, nullable=False)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

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

    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # returning id for now. Method to return all counts?
        return self.id

class Round(Base):
    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    ongoing = db.Column(db.Boolean, nullable=False)
    throwcount = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        # returning id for now. Need to return other?
        return self.id

class Throw(Base):
    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    hit = db.Column(db.Integer, nullable=False)
    mod = db.Column(db.Integer, nullable=False)

    round_id = db.Column(db.Integer, db.ForeignKey('round.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        sum = self.hit * self.mod
        return str(sum)

class LastThrows(Base):
    player_id = db.Column(db.Integer, db.ForeignKey('player.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    counts = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str(self.counts)
