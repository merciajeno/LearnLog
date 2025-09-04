import datetime

import firebase_admin
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials,auth, firestore

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate('learnlog.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def verify_user(func):
    def wrapper(*args, **kwargs):
        id_token = request.headers.get("Authorization")
        if not id_token:
            return jsonify({"error": "Missing token"}), 401
        try:
            decoded_token = auth.verify_id_token(id_token)
            request.user = decoded_token
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/protected')
def func():
    return jsonify({"message":"Hello"})
from flask import Flask, request, jsonify
import datetime
from firebase_admin import firestore

@app.route('/add_user', methods=['POST'])
def create_user_in_firestore():
    data = request.get_json()
    uid = data['uid']
    email = data['email']

    user_ref = db.collection("users").document(uid)
    if not user_ref.get().exists:  # only create if new
        user_ref.set({
            "email": email,
            "streak": 0,
            "lastLogged": None,
            "createdAt": datetime.datetime.now()
        })
    return jsonify({"message": "success"}), 200


@app.route("/add_subject", methods=["POST"])
def add_subject():
    data = request.get_json()
    user_id = data["user_id"]
    subject_name = data["name"]

    subject_ref = db.collection("users").document(user_id).collection("subjects").document()
    subject_ref.set({
        "name": subject_name,
        "createdAt": datetime.datetime.now()
    })

    return jsonify({"message": "Subject added!"}), 200


@app.route("/add_log", methods=["POST"])
def add_log():
    data = request.get_json()
    user_id = data["user_id"]
    subject_id = data["subject_id"]
    content = data["content"]

    user_ref = db.collection("users").document(user_id)
    user_data = user_ref.get().to_dict()

    today = datetime.datetime.now().date()
    last_logged = user_data.get("lastLogged")

    # Update streak
    if last_logged:
        last_logged_date = last_logged.date()
        if (today - last_logged_date).days == 1:
            # Continue streak
            new_streak = user_data["streak"] + 1
        elif (today - last_logged_date).days == 0:
            # Already logged today → don't increment
            new_streak = user_data["streak"]
        else:
            # Streak broken
            new_streak = 1
    else:
        new_streak = 1

    # Save log
    log_ref = (
        db.collection("users")
        .document(user_id)
        .collection("subjects")
        .document(subject_id)
        .collection("logs")
        .document()
    )
    log_ref.set({
        "content": content,
        "date": datetime.datetime.now()
    })

    # Update user
    user_ref.update({
        "streak": new_streak,
        "lastLogged": datetime.datetime.now()
    })

    return jsonify({"message": "Log added!"}), 200

@app.route("/update_subject",methods=["PUT"])
def update_subject():
    data = request.get_json()
    user_id = data['user_id']
    subject_id = data['subject_id']
    name = data['name']
    sub_ref = (
        db.collection("users")
        .document(user_id)
        .collection("subjects")
        .document(subject_id)

    )

    sub_ref.update({
        "name":name
    })


@app.route("/update_log", methods=["PUT"])
def update_log():
    data = request.get_json()
    log_id = data['log_id']
    user_id = data['user_id']
    subject_id = data['subject_id']
    content = data['content']

    log_ref = (
        db.collection("users")
        .document(user_id)
        .collection("subjects")
        .document(subject_id)
        .collection("logs")
        .document(log_id)
    )

    # Update only content + date (streak unchanged here)
    log_ref.update({
        "content": content,
        "date": datetime.datetime.now()
    })

    return jsonify({"message": "Log updated!"}), 200

@app.route('/dashboard/<user_id>', methods=['GET'])
def dashboard(user_id):
    user_doc = db.collection("users").document(user_id).get()
    if not user_doc.exists:
        return jsonify({'message': 'User not found'}), 404

    user_data = user_doc.to_dict()
    streak = user_data.get("streak", 0)

    subjects_ref = db.collection("users").document(user_id).collection("subjects").stream()
    log_count = 0
    today = datetime.datetime.now()

    for subject in subjects_ref:
        logs_ref = (
            db.collection("users")
            .document(user_id)
            .collection("subjects")
            .document(subject.id)
            .collection("logs")
            .stream()
        )
        for log in logs_ref:
            log_data = log.to_dict()
            log_date = log_data.get("date")
            
            if log_date:
                if log_date == today:
                    log_count += 1

    return jsonify({
        "streak": streak,
        "today_logs": log_count
    }), 200

@app.route('/get_subjects/<user_id>', methods=['GET'])
def get_subjects(user_id):
    print(user_id)
    user_doc = db.collection("users").document(user_id).get()

    if not user_doc.exists:
        return jsonify({'message': 'User not found'}), 404

    subjects_ref = db.collection("users").document(user_id).collection("subjects").stream()
    subjects = [{"id": subj.id, **subj.to_dict()} for subj in subjects_ref]

    return jsonify({"subjects": subjects}), 200

@app.route("/users/<user_id>/subjects/<subject_id>/logs", methods=["GET"])
def get_logs(user_id, subject_id):
    subject = db.collection("users").document(user_id).collection("subjects").document(subject_id).get()
    if not subject.exists:
        return jsonify({"error":"Subject not found"})
    logs = (
        db.collection("users")
        .document(user_id)
        .collection("subjects")
        .document(subject_id)
        .collection("logs")
        .stream()
    )
    log_list = [{"id": l.id, **l.to_dict()} for l in logs]
    return jsonify({"logs": log_list})


@app.route("/delete_subject/<user_id>/<subject_id>", methods=["DELETE"])
def delete_subject(user_id, subject_id):
    logs = db.collection("users").document(user_id).collection("subjects").document(subject_id).collection(
        "logs").stream()
    for log in logs:
        log.reference.delete()

    # then delete subject
    db.collection("users").document(user_id).collection("subjects").document(subject_id).delete()

    return jsonify({"message": "Subject deleted!"}), 200


@app.route("/delete_log/<user_id>/<subject_id>/<log_id>",methods=["DELETE"])
def delete_log(user_id,subject_id,log_id):
    db.collection("users").document(user_id).collection("subjects").document(subject_id).collection("logs").document(log_id).delete()
    return jsonify({"message":"Log deleted"}), 200

if __name__=='__main__':
    app.run(debug=True)