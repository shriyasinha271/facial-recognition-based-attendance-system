# Facial Recognition Attendance (OpenCV LBPH)


Lightweight, offline attendance system using OpenCV's LBPH face recognizer. No cloud, no paid APIs. Ideal for college projects and small offices.


## Features
- ✅ Offline, fast, low-dependency
- ✅ Webcam-based, marks once per person per day
- ✅ SQLite + CSV export
- ✅ Dataset tools to collect & train


## Setup
```bash
# 1) Clone
git clone https://github.com/<your-username>/facerec-attendance.git
cd facerec-attendance


# 2) Create venv
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate


# 3) Install
pip install -r requirements.txt


# 4) Make folders
mkdir -p data/raw data/models data/attendance/logs