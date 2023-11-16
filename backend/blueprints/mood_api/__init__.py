from flask import Flask, Blueprint, request, jsonify
import mysql.connector
from mysql.connector import errorcode
import sys
sys.path.append(sys.path[0][:-len('\\backend')] + '/database')
from mysql_connection import mysql_connect

blueprint = Blueprint('mood_api', __name__, url_prefix='/mood_api')

@blueprint.route('/get_user_mood/<int:user_id>', methods=['GET'])
def get_user_mood(user_id):
    try:
        db, cursor = mysql_connect()

        query = "SELECT * FROM Mood WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        user_mood = cursor.fetchall()
        cursor.close()
        
        return jsonify({'user_mood': user_mood}), 200
    except Exception as e:
        return jsonify({'error': str(e)})

@blueprint.route('/add_user_mood', methods=['POST'])
def add_user_mood():
    try:
        user_id = request.json['user_id']
        user_happiness = request.json['user_happiness']
        user_motivation = request.json['user_motivation']
        date = request.json['date']

        db, cursor = mysql_connect()

        query = "INSERT INTO Mood (Happiness, Motivation, UserID, Time) VALUES (%s, %s, %s,%s)"
        data = (user_happiness, user_motivation, user_id, date)
        cursor.execute(query, data)
        
        cursor.close()
        db.commit()

        return jsonify({"message": "Mood added successfully."}), 200
    except Exception as e:
        return jsonify({'error': str(e)})
    
@blueprint.route('/update_user_mood', methods=['PUT'])
def update_user_mood():
    try:
        user_id = request.json['user_id']
        user_happiness = request.json['user_happiness']
        user_motivation = request.json['user_motivation']
        date = request.json['date']

        db, cursor = mysql_connect()
        
        query = "UPDATE Mood SET Happiness = %s, Motivation = %s, Time = %s WHERE UserID = %s"
        data = (user_happiness, user_motivation, date, user_id)
        cursor.execute(query, data)
        
        cursor.close()
        db.commit()
        
        return jsonify({"message": "Mood updated successfully."}), 200
    except Exception as e:
        return jsonify({'error': str(e)})