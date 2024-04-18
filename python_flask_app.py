from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongo', 27017)  # Подключение к контейнеру с монго

db = client.mydatabase  # Используемая бд
collection = db.mycollection  # Используемая коллекция

@app.route('/<key>', methods=['GET', 'PUT', 'POST'])
def handle_key(key):
    if request.method == 'GET':
        # Чтение значения из бд по ключу
        result = collection.find_one({'_id': key})
        if result:
            return jsonify({key: result['value']}), 200
        else:
            return jsonify({'error': 'Key not found'}), 404
    elif request.method == 'PUT':
        # Изменение значения в бд по ключу
        data = request.get_json()
        if 'value' in data:
            result = collection.update_one({'_id': key}, {'$set': {'value': data['value']}}, upsert=True)
            if result.modified_count > 0:
                return jsonify({'message': 'Value updated successfully'}), 200
            else:
                return jsonify({'error': 'Failed to update value'}), 500
        else:
            return jsonify({'error': 'Value not provided'}), 400
    elif request.method == 'POST':
        # Создание новой записи в бд
        data = request.get_json()
        if 'value' in data:
            result = collection.insert_one({'_id': key, 'value': data['value']})
            if result.inserted_id:
                return jsonify({'message': 'Value created successfully'}), 201
            else:
                return jsonify({'error': 'Failed to create value'}), 500
        else:
            return jsonify({'error': 'Value not provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)