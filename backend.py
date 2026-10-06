from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)

#database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///games.db" #games db
app.secret_key = "idk"
app.permanent_session_lifetime = timedelta(days=30)
db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='games') #link user to game
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

with app.app_context():
    db.create_all()


#routes
@app.route("/")
def root():
    if not loggedIn():
        return jsonify({"message":"Not logged in"}), 401
    return jsonify({"message": f"Welcome, {session['username']}!"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session["user_id"] = user.id
        session["username"] = user.username
        return jsonify({"message": "Successfully logged in"}), 200
    return jsonify({"error": "Invalid login"}), 401

def loggedIn():
    return "user_id" in session

@app.route("/logout", methods=["POST"])
def logout():
    if not loggedIn():
        return {"error": "No login cookie"}, 401
    session.clear()
    return jsonify({"message": "Successfully logged out"}), 200

@app.route("/create-account", methods=["POST"])
def create_account():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    if User.query.filter_by(username=username).first(): #check for existing users with same name
        return jsonify({"error": "Username already exists"}), 409
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Account created"}), 201


@app.route("/games",methods=["GET"])
def get_games():
    if not loggedIn():
        return jsonify({"message":"Not logged in"}), 401
    games = Game.query.filter_by(user_id=session["user_id"]).all()
    return jsonify([game.to_dict() for game in games]), 200

@app.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id):
    if not loggedIn():
        return jsonify({"message":"Not logged in"}), 401
    game = Game.query.filter_by(id=game_id, user_id=session["user_id"]).first()
    if game:
        return jsonify(game.to_dict()), 200
    return jsonify({"error": "Game not found"}), 404

@app.route("/create-game", methods=["POST"])
def create_game():
    if not loggedIn():
        return jsonify({"message":"Not logged in"}), 401
    data = request.get_json()
    new_game = Game(user_id=session["user_id"],
                    name=data["name"],
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
    if not loggedIn():
        return jsonify({"message":"Not logged in"})
    game = Game.query.filter_by(id=game_id, user_id=session["user_id"]).first()
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
    if not loggedIn():
        return jsonify({"message":"Not logged in"})
    game = Game.query.filter_by(id=game_id, user_id=session["user_id"]).first()
    if game:
        db.session.delete(game)
        db.session.commit()
        return jsonify({"message": f"Deleted game {game_id}"}), 200
    return jsonify({"error": "Game not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)