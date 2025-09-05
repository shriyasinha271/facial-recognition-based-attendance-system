import os
import json
import argparse
from datetime import date


import cv2


from utils.db import get_conn, mark_today, export_day_csv


CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
MODEL_PATH = os.path.join("data", "models", "lbph_model.xml")
LABELS_PATH = os.path.join("data", "models", "labels.json")




def load_model():
if not os.path.exists(MODEL_PATH) or not os.path.exists(LABELS_PATH):
raise SystemExit("Model not found. Train first: python scripts/train_model.py")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)
with open(LABELS_PATH, "r", encoding="utf-8") as f:
labels = {int(k): v for k, v in json.load(f).items()}
return recognizer, labels




def run(camera_idx: int = 0, threshold: float = 70.0):
recognizer, labels = load_model()
conn = get_conn()


cap = cv2.VideoCapture(camera_idx)
if not cap.isOpened():
raise SystemExit("Could not open camera")


print("[INFO] Press 'q' to quit")
while True:
ret, frame = cap.read()
if not ret:
continue
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = CASCADE.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))


for (x, y, w, h) in faces:
face = gray[y:y+h, x:x+w]
face = cv2.resize(face, (200, 200))
label_id, confidence = recognizer.predict(face)
name = labels.get(label_id, "Unknown")


if confidence < threshold and name != "Unknown":
newly_marked = mark_today(conn, name)
status = "MARKED" if newly_marked else "ALREADY"
text = f"{name} ({status})"
color = (0, 255, 0) if newly_marked else (0, 200, 255)
else:
text = "Unknown"
color = (0, 0, 255)


cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)


cv2.imshow("Attendance", frame)
if cv2.waitKey(1) & 0xFF == ord('q'):
ap.add_argument("--threshold", type=float, default=70.0, help="LBPH