import cv2
import os
import argparse
import time


CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")




def sanitize(name: str) -> str:
return name.strip().replace(" ", "_")




def main():
ap = argparse.ArgumentParser(description="Collect face images for a person")
ap.add_argument("--person", required=True, help="Person name")
ap.add_argument("--samples", type=int, default=60, help="Number of images to capture")
ap.add_argument("--camera", type=int, default=0, help="Camera index")
args = ap.parse_args()


person_dir = os.path.join("data", "raw", sanitize(args.person))
os.makedirs(person_dir, exist_ok=True)


cap = cv2.VideoCapture(args.camera)
if not cap.isOpened():
raise SystemExit("Could not open camera")


count = 0
print("[INFO] Look at the camera. Press 'q' to quit.")
while count < args.samples:
ret, frame = cap.read()
if not ret:
continue


gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = CASCADE.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))


for (x, y, w, h) in faces:
face = gray[y:y+h, x:x+w]
face = cv2.resize(face, (200, 200))
path = os.path.join(person_dir, f"{int(time.time()*1000)}.png")
cv2.imwrite(path, face)
count += 1
cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.putText(frame, f"Saved: {count}/{args.samples}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
if count >= args.samples:
break


cv2.imshow("Collect Faces", frame)
if cv2.waitKey(1) & 0xFF == ord('q'):
break


cap.release()
cv2.destroyAllWindows()
print(f"[DONE] Saved {count} images to {person_dir}")




if __name__ == "__main__":
main()