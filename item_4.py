"""
Item 4.
Write an API server that meets the following requirements:

1. Login
    a) POST /api/login
    b) Inputs are username and password in JSON
    c) Case insensitively validates usernames with at least 4 
    letters and the letters “a”, “b”, and “c” are in the 
    username in that order. Please see the example below 
        i.  abacca is validated
        ii. Cabbie is not validated since there is no c that comes after ab
        iii.Acaiberrycake is valid
    d) Password will be valid if it is equal to the reverse of the username

2. List letters
    a) GET /api/letters
    b) Seed your database with the following data (you may use an in memory 
    data or use a third party database application. If you do use an external 
    database, make sure that it is included in the submission by submitting a
    docker image)
        i.  {“letter”:”A”, “value”:1, “strokes”:2, “vowel”:true},{“letter”:”B”, 
        “value”:2, “strokes”:1, “vowel”:false}
        ii. You may represent the data in your database however you like as 
        long as the expected API outputs are met
    c) This should return a json of all unique letters in the database sorted 
    by value in ascending order. Given the seed data, this should return 
    {“letters”:[“A”, “B”]}

3. Add letter
    a) POST /api/letter/add
    b) Input is a json object containing the following fields:
        i.  Letter: string
        ii. Value: int - any random value
        iii.Strokes: int - any number that is not equal to value
        iv. Vowel: bool - if the letter is treated as a vowel or not
    c) Letters must be unique and not limited to the latin alphabet
        i.  Hence a request with {“letter”:”A”, “value”:1, “strokes”:2, “vowel”:true} will fail
    d) Return {‘status”:0} if the letter was added to the database otherwise return {“status”:1}

4. Get letter
    a) GET /api/letter/<letter:str>
    b) Returns the details of the letter in the URL
        i.  /api/letter/A will return {“letter”:”A”, “value”:1, “strokes”:2, “vowel”:true}

        
5. Shuffle letters
    a) GET /api/letter/shuffle
    b) Returns a string containing all the letters in the database without repetition but in a random order
    c) Plus points will be given for implementing your own shuffle function

6. Filter letters
    a) GET /api/letter/filter/<val:int>
    b) Returns a list of letters whose value field is less than or equal to val ordered by when they were added to the database
    c) On the original set, accessing /api/letter/filter/1 this should return {“letters”:[“A”]}
"""

from flask import Flask, request, jsonify
import random
from typing import Dict, List
app = Flask(__name__)

# In-memory database
letters_db: List[Dict[str, any]] = [
    {"letter": "A", "value": 1, "strokes": 2, "vowel": True},
    {"letter": "B", "value": 2, "strokes": 1, "vowel": False}
]

def validate_username(username: str) -> bool:

    username = username.lower()
    
    # Check if length is at least 4 and 'a', 'b', and 'c' are present in the correct order
    if 'a' in username and 'b' in username and 'c' in username and len(username) >= 4:
        a_index = username.index('a')
        b_index = username.index('b')
        c_index = username.index('c')
        return a_index < b_index < c_index
    
    # If any condition fails, return False
    return False

def custom_shuffle(letters: str) -> str:
    """
    Shuffles the letters and returns them as a string.
    """
    # Remove duplicates
    unique_letters = list(set(letters))

    # Shuffle the letters
    for i in range(len(unique_letters) - 1, 0, -1):
        j = random.randint(0, i)
        unique_letters[i], unique_letters[j] = unique_letters[j], unique_letters[i]

    return unique_letters

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validate username
    if not validate_username(username):
        return jsonify({"error": "Invalid username"})

    # Check if the password is the reverse of the username
    if not password == username[::-1]:
        return jsonify({"error": "Invalid password"})

    return jsonify({"message": "Login details valid"})

@app.route('/api/letters', methods=['GET'])
def list_letters():
    # Sort letters by ascending value
    sorted_letters = sorted(letters_db, key=lambda x: x['value'])
    return jsonify({"letters": [letter['letter'] for letter in sorted_letters]})

@app.route('/api/letter/add', methods=['POST'])
def add_letter():
    data = request.get_json()
    letter = data.get('letter')
    value = data.get('value')
    strokes = data.get('strokes')
    vowel = data.get('vowel')

    #validate letter, value, strokes, and vowel
    if not isinstance(letter, str) or not isinstance(value, int) or (not isinstance(strokes, int) and strokes == value) or not isinstance(vowel, bool):
        return jsonify({"status": 1})

    # Check for uniqueness
    if any(each['letter'] == letter for each in letters_db):
        return jsonify({"status": 1})

    # Add the letter to the database
    letters_db.append({"letter": letter, "value": value, "strokes": strokes, "vowel": vowel})
    return jsonify({"status": 0})

@app.route('/api/letter/<letter>', methods=['GET'])
def get_letter(letter: str):
    # Find the letter in the database and return its details
    for each in letters_db:
        if each['letter'].lower() == letter.lower():
            return jsonify(each)
        
    # If the letter is not found, return an error
    return jsonify({"error": "Letter not found"})

@app.route('/api/letter/shuffle', methods=['GET'])
def shuffle_letters():
    # Get all letters from the database
    letters = [l['letter'] for l in letters_db]
    
    # Shuffle the letters using a custom shuffle function
    shuffled_letters = custom_shuffle(''.join(letters))

    return jsonify(shuffled_letters)

@app.route('/api/letter/filter/<int:val>', methods=['GET'])
def filter_letters(val: int):
    # create a list of letters that has less than or equal to val
    filtered_letters = [l['letter'] for l in letters_db if l['value'] <= val]

    return jsonify({filtered_letters})

if __name__ == '__main__':
    app.run(debug=True)
    