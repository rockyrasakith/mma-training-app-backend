from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from random import choice

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URL"))
db = client.mma

# Check DB Route
@app.route('/check_db')
def check_db():
    try:
        # check if we can connect to the server
        client.server_info()
        return jsonify({"status": "success", "message": "MongoDB is connected"})
    except Exception as e:
        return jsonify({"status": "error", "message": "Failed to connect to MongoDB", "error": str(e)})

# Create users
@app.route('/new_user', methods=['POST'])
def create_user():
    data = request.get_json()
    print("Data received: ", data)
    name = data.get('name')
    email = data.get('email')
    user = {
        "name": name,
        "email": email,
    }
    users_collection = db.users
    result = users_collection.insert_one(user)
    return jsonify({"message": "User created", "user_id": str(result.inserted_id)})

# Create a new workout
@app.route('/create_workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    print("Data received: ", data)
    workout_name = data.get("name")
    workout_position = data.get("position")
    exercise_1_name = data.get("exercise_1_name")
    exercise_2_name = data.get("exercise_2_name")
    exercise_3_name = data.get("exercise_3_name")
    exercise_1_reps = int(data.get("exercise_1_reps"))
    exercise_2_reps = int(data.get("exercise_2_reps"))
    exercise_3_reps = int(data.get("exercise_3_reps"))
    workout = {
        "name": workout_name,
        "workout_position": workout_position,
        "exercise_1": exercise_1_name,
        "exercise_2": exercise_2_name,
        "exercise_3": exercise_3_name,
        "exercise_1_reps": exercise_1_reps,
        "exercise_2_reps": exercise_2_reps,
        "exercise_3_reps": exercise_3_reps,
    }
    workouts_collection = db.workouts
    result = workouts_collection.insert_one(workout)
    return jsonify({"message": "Workout created", "workout_id": str(result.inserted_id)})


# Generate a random workout
@app.route('/random_workout')
def random_workout():
    workouts_collection = db.workouts
    workouts = list(workouts_collection.find({},{'_id':0}))
    random_workout = choice(workouts)
    return jsonify(random_workout)


# Check users
@app.route('/users')
def users():
    users_collection = db.users
    users = list(users_collection.find({},{'_id':0}))
    return jsonify(users)

# Main Route
@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
