from flask import Flask, Response, render_template, send_from_directory
import base64
import cv2
import os

app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_b64 = base64.b64encode(buffer).decode('utf-8')
        yield f"data: {frame_b64}\n\n"
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image/<filename>')
def serve_image(filename):
    return send_from_directory('image', filename)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
