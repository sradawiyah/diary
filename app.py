from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb+srv://sradawiyah27:akuobi123@cluster0.j1o6zjr.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    #sample_receive = request.args.get('sample_give')
    #print(sample_receive)
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    save_to = f'static/post-{mytime}.{extension}'
    file.save(save_to)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    prosave_to = f'static/profile-{mytime}.{extension}'
    file.save(prosave_to)


    doc = {
    'file': save_to,
    'profile': prosave_to,
    'title': title_receive,
    'content': content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'data tersimpan!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)