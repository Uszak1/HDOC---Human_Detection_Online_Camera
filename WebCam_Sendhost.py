from flask import Flask, Response
import cv2

app = Flask(__name__)

def find_cameras():
    available_cameras = []
    for i in range(10):
        camera = cv2.VideoCapture(i)
        if camera.isOpened():
            available_cameras.append(i)
            camera.release()
    return available_cameras

cameras = find_cameras()
if cameras:
    last_camera_index = cameras[-1]
    camera = cv2.VideoCapture(last_camera_index)
    if not camera.isOpened():
        exit()
else:
    exit()


def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)