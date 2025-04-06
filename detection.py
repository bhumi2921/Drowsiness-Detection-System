# detection.py
import cv2
import time

# Haar cascades
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

# Thresholds
CLOSE_TIME_THRESHOLD = 2  # seconds
eye_closed_start_time = None
drowsiness_status = {"drowsy": False}
camera_active = {"status": False}

def reset_drowsiness():
    global eye_closed_start_time
    eye_closed_start_time = None
    drowsiness_status["drowsy"] = False

def generate_frames():
    global eye_closed_start_time
    cap = cv2.VideoCapture(0)
    camera_active["status"] = True

    while camera_active["status"]:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        eyes_closed = False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5, minSize=(30, 30))
            if len(eyes) == 0:
                eyes_closed = True
                break

        if eyes_closed:
            if eye_closed_start_time is None:
                eye_closed_start_time = time.time()
            elif time.time() - eye_closed_start_time >= CLOSE_TIME_THRESHOLD:
                drowsiness_status["drowsy"] = True
        else:
            eye_closed_start_time = None
            drowsiness_status["drowsy"] = False

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
    reset_drowsiness()
