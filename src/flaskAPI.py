from flask import Flask, jsonify, request
from src.Log import Log
import os

def getCsv(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data
app = Flask(__name__)


def getVideo():
    video_path = "../video_enregistrement.mp4" 

    if os.path.exists(video_path):
        return video(video_path, mimetype="video/mp4")
    else:
        return jsonify({"error": "Video not found"}), 404

@app.route('/video', methods=['GET'])
def video():
    try:
        video = getVideo()
        return jsonify({"video": video}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def getVideo():
    # Placeholder function to simulate video retrieval
    return "Video content or URL"
    

@app.route('/mail', methods=['POST'])
def mail():
    try :
        Log(path = 'src/Data/presence_log.csv')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return "Mail send", 200

@app.route('/log', methods=['GET'])
def log():
    return getCsv('src/Data/presence_log.csv'), 200


def main_api():
    app.run(host='0.0.0.0', port=5000)

main_api()