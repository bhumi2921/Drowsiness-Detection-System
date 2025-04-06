# app.py
from flask import Flask, render_template, Response, jsonify
from detection import generate_frames, drowsiness_status, camera_active

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    return jsonify({"drowsy": drowsiness_status["drowsy"]})

@app.route('/start')
def start():
    camera_active["status"] = True
    return ('', 204)

@app.route('/stop')
def stop():
    camera_active["status"] = False
    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True)
