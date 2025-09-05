import os
import json
import cv2
import numpy as np


RAW_DIR = os.path.join("data", "raw")
MODEL_DIR = os.path.join("data", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "lbph_model.xml")
LABELS_PATH = os.path.join(MODEL_DIR, "labels.json")


os.makedirs(MODEL_DIR, exist_ok=True)


recognizer = cv2.face.LBPHFaceRecognizer_create(radius=2, neighbors=10, grid_x=8, grid_y=8)


images, labels = [], []
label_map = {}
current_label = 0


for person_name in sorted(os.listdir(RAW_DIR)):
person_dir = os.path.join(RAW_DIR, person_name)
if not os.path.isdir(person_dir):
continue
label_map[current_label] = person_name
for fname in os.listdir(person_dir):
if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
continue
path = os.path.join(person_dir, fname)
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
if img is None:
continue
img = cv2.resize(img, (200, 200))
images.append(img)
labels.append(current_label)
current_label += 1


if not images:
raise SystemExit("No training data found. Run collect_faces.py first.")


recognizer.train(images, np.array(labels))
recognizer.save(MODEL_PATH)


with open(LABELS_PATH, "w", encoding="utf-8") as f:
json.dump(label_map, f, indent=2)


print(f"[OK] Trained LBPH model → {MODEL_PATH}")
print(f"[OK] Labels → {LABELS_PATH}")