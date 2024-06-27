# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here

@app.route("/games")
def games():
    games_dict = [game.to_dict() for game in Game.query.order_by(Game.title).all()]
    response = make_response(
        games_dict,200, {"Content-Type":"application/json"})
    return response

@app.route("/games/<int:id>")
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    if game:
        body = game.to_dict()
        status = 200
    else:
        body = {"message" : f"Game id {id} does not exist"}
        status = 404

    response = make_response(body,status,{"Content-Type":"application/json"})
    return response

@app.route("/games/users/<int:id>")
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    if game:
        body = [user.to_dict(rules = ("-reviews",) ) for user in game.users]
        status = 200
    else:
        body = {"message": f"Game {id} not found"}
        status = 404
    
    response = make_response(body,status,{"Content-Type":"application/json"})
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

