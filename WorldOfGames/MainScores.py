# run with commend : flask --app MainScores.py run
import werkzeug
from flask import Flask, render_template , request, redirect ,url_for, jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='template')

# MongoDB connection details
mongo_host = 'mongodb'
mongo_port = 27017  # Default MongoDB port
# mongo_username = 'your_username'
# mongo_password = 'your_password'
mongo_database = 'monogodb'

def get_collections():
    client = MongoClient(host=mongo_host,
                     port=mongo_port,
                    #  username=mongo_username,
                    #  password=mongo_password,
                     authSource=mongo_database
                        )
    db = client.get_database()
    return db

def read_score(player):
    # List all collections
    collections = get_collections()
    # collections = db.list_collection_names()
    # print("Collections:")
    # for collection in collections:
        # print(collection)
    return collections
    # Retrieve the user's score from the database  
    # if db.find_one(player):
    #     score = user_data['score']
    #     return jsonify(score)
    # else:
    #     return None
        # except Exception as e:
        #     return jsonify({'error': str(e)})


def add_score(diff,player):
    # add the points_of_winning to score
    cur_score = read_score(player)
    new_score = cur_score + ((diff * 3) + 5)
    print(f"your new score is {new_score}")
    write_score(player,new_score)

def write_score(player, new_score):
    # Update the user's score in the database
    get_users_collection().update_one(
        {'name': player},
        {'$set': {'score': new_score}},
        upsert=True
    )    

@app.route('/')
def content():
    return render_template('get_score.html')

# Route to handle the form submission and display the player's score
@app.route('/get_score', methods=['get'])
def get_score():
    player = request.args.get('player')
    score = read_score(player)
    return render_template('index.html', player=player, score=score)



@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return render_template('error.html', message=f"file not found!")


app.register_error_handler(500, handle_bad_request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
