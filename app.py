from flask import Flask, render_template, request, redirect, url_for ,jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime, timedelta
from flask_cors import CORS



app = Flask(__name__,template_folder="templates")
CORS(app,origins="*")

app.config["MONGO_URI"] = "mongodb://localhost:27017/todo"
mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


# Function to serialize ObjectId to string for JSON response
def serialize_task(task):
    task['_id'] = str(task['_id'])
    return task


@app.route("/task", methods=["POST"])
def create_task():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        id = data.get("_id")
        name = data.get('name')
        status = data.get('status')
        priority = data.get('priority')
        due_date = data.get('due_date')

        if name or status or priority or due_date:
            task = {
                'name': name,
                'status': status,
                'priority': priority,
                'due_date': due_date
            }

            if not id:
                task_id = mongo.db.tasks.insert_one(task).inserted_id
                return jsonify({'message': 'Task created successfully', 'task_id': str(task_id)}), 201
            else:
                update_task(id, task)
                return jsonify({'message': 'Task updated successfully'}), 200
        else:
            return jsonify({'error': 'Incomplete data provided'}), 400

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500


def update_task(task_id, update_data):
    try:
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': update_data})
        return jsonify({'message': 'Task updated successfully', 'task_id': str(task_id)}), 201

    except Exception as e:
        raise Exception('Error updating task: {}'.format(str(e)))


# Route to delete a task
@app.route('/task/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = mongo.db.tasks.delete_one({'_id' : ObjectId(task_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404


# Route to get all tasks
@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    tasks = list(mongo.db.tasks.find())
    serialized_tasks = [serialize_task(task) for task in tasks]
    return jsonify(serialized_tasks), 200

# Route to get tasks priority-wise
@app.route("/tasks/priority/<string:priority>", methods=["GET"])
def get_tasks_by_priority(priority):
    tasks = list(mongo.db.tasks.find({'priority': priority}))
    serialized_tasks = [serialize_task(task) for task in tasks]
    return jsonify(serialized_tasks), 200

# Route to get tasks due today
@app.route("/tasks/today", methods=["GET"])
def get_tasks_due_today():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    tasks = list(mongo.db.tasks.find({'due_date': {'$gte': today, '$lt': tomorrow}}))
    serialized_tasks = [serialize_task(task) for task in tasks]
    return jsonify(serialized_tasks), 200


