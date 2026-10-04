from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///games.db"

db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genres = db.Column(db.JSON, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    full_completion = db.Column(db.Boolean, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "completed": self.completed,
            "full_completion": self.full_completion,
            "hours": self.hours,
            "rating": self.rating,
            "review": self.review
        }

with app.app_context():
    db.create_all()


#routes
@app.route("/")
def root():
    return jsonify({"message":"Is this message good? No!"})

@app.route("/games",methods=["GET"])
def get_games():
    games = Game.query.all()
    return jsonify([game.to_dict() for game in games]), 200

@app.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id):
    game = Game.query.get(game_id)
    if game:
        return jsonify(game.to_dict()), 200
    return jsonify({"error": "Game not found"}), 404

@app.route("/create-game", methods=["POST"])
def create_game():
    data = request.get_json()
    new_game = Game(name=data["name"],
                    genres=data["genres"],
                    completed=data["completed"],
                    full_completion=data["full_completion"],
                    hours=data["hours"],
                    rating=data["rating"],
                    review=data["review"])
    db.session.add(new_game)
    db.session.commit()
    return jsonify(new_game.to_dict()), 201

@app.route("/update-game/<int:game_id>", methods=["PUT"])
def update_game(game_id):
    game = Game.query.get(game_id)
    if game:
        data = request.get_json()
        game.name = data["name"]
        game.genres = data["genres"]
        game.completed = data["completed"]
        game.full_completion = data["full_completion"]
        game.hours = data["hours"]
        game.rating = data["rating"]
        game.review = data["review"]
        db.session.commit()
        return jsonify(game.to_dict()), 200
    return jsonify({"error": "Game not found"}), 404

@app.route("/delete/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
        return jsonify({"message": f"Deleted game {game_id}"}), 200
    return jsonify({"error": "Game not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)