from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_restful import Api, Resource
from flask import Flask, request, jsonify, render_template
from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__, template_folder="templates")

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://opqqmwkj:TcR4WyPVA6PJRdI7DPjk4NW27D3NzpHb@stampy.db.elephantsql.com/opqqmwkj'

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    return "Welcome to the API!" 
@app.route('/register', methods=['GET'])
def show_registration_page():
    return render_template('registration.html')

@app.route('/change_username', methods=['GET', 'POST'])
def change_username():
    if request.method == 'POST':
        new_username = request.form.get('new-username')
        # Update the user's username in the database (you need to add this logic)

        # After updating the username, you can redirect the user to another page, e.g., the profile page
        return redirect(url_for('profile'))  # Change 'profile' to your actual route

    return render_template('change_username.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Add your authentication logic here (verify username and password)

        if authentication_succeeds:  # Implement your authentication logic
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    elif request.method == 'GET':
        # Handle the GET request (e.g., display a login form)
        return render_template('login.html')




@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username is already taken"}), 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')

#         # Add your authentication logic here (verify username and password)

#         if authentication_succeeds:  # Implement your authentication logic
#             access_token = create_access_token(identity=user.id)
#             return jsonify(access_token=access_token), 200
#         else:
#             return jsonify({"message": "Invalid username or password"}), 401

@app.route('/change_username', methods=['PUT'])
@jwt_required
def change_username():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    new_username = request.get_json().get('new_username')
    if User.query.filter_by(username=new_username).first():
        return jsonify({"message": "Username is already taken"}), 400

    user.username = new_username
    db.session.commit()

    return jsonify({"message": "Username changed successfully"}), 200

# Define the User model with a serialize method
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120))

    # Define a relationship with PokemonCatched (one-to-many)
    pokemon_catched = db.relationship('PokemonCatched', back_populates='user')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
        }

# Define the Pokemon model
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

# Define the PokemonCatched model
class PokemonCatched(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)

    user = db.relationship('User', back_populates='pokemon_catched')
    pokemon = db.relationship('Pokemon')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pokemon_id': self.pokemon_id,
        }

class UserResource(Resource):
    @jwt_required
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user.serialize()), 200
        return jsonify({"message": "User not found"}), 404

class PokemonResource(Resource):
    def get(self, pokemon_id):
        pokemon = Pokemon.query.get(pokemon_id)
        if pokemon:
            return jsonify(pokemon.serialize()), 200
        return jsonify({"message": "Pokemon not found"}), 404

# Define resources and CRUD methods for PokemonCatched as needed

if __name__ == '__main__':
    app.run(debug=True)
