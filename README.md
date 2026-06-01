# Rubik Cube Solver App

A Python-based application for interacting with and solving the Rubik’s Cube using manual input, camera-assisted color detection, and an external solving algorithm.

---

## ⚠️ Status
This project is under active development and some features are experimental.

## 🚀 Features

### 🎮 GUI Interface
- Manual input of Rubik’s Cube colors via a visual cube layout
- Reset functionality
- Basic controls for solving and session handling

### 📷 Camera-Based Color Detection
- Integration with external camera sources (e.g. DroidCam)
- Region of Interest (ROI) detection for extracting cube face colors (`roi.py`)
- Detection of 3x3 cube stickers from video stream (basic implementation)
- Experimental feature (not fully automated yet)

### 🔀 Scramble Generator
- Generates Rubik’s Cube scrambles using Singmaster notation (R, U, R', U', etc.)

### ⏱ Timer & Move Tracking
- Simple speedcubing timer
- Manual move input tracking (notation-based)
- Stores solve sessions and move history

### 💾 Data Storage
- Saves solve sessions locally
- Stores move sequences for later analysis
- Basic export support (e.g. Excel / database format)

### 🌐 Backend API
- Built with Django and Django REST Framework
- Provides endpoints for processing cube data and solving requests
- Communication layer between GUI and backend logic

---

## 🧠 Core Solving Engine

This project uses the **Kociemba Two-Phase Algorithm** to generate efficient solutions for the Rubik’s Cube (typically around ~19 moves in optimal cases).

Based on:

https://github.com/hkociemba/RubiksCube-TwophaseSolver

---

## 🛠 Tech Stack

- Python
- Django + Django REST Framework (backend API)
- OpenCV
- Tkinter / PyQt (GUI)
- NumPy / Pandas
- RubikTwoPhase (Kociemba solver)

---

## 📁 Project Structure

- `src/` – main application code
  - `client/` – GUI application (gui.py)

- `legacy/` – older or experimental code kept for reference
- `scripts/` – helper utilities and scripts

- `requirements.txt` – project dependencies
- `README.md` – documentation
- `LICENSE` – project license (GPLv3)
- `.gitignore` – ignored files

---

## ▶️ How to Run

### Backend (Django server)
```bash
python manage.py runserver
```
### GUI (client application)
```bash
python client/gui.py
```
## 📌 Future Improvements
- Full automatic cube reconstruction from camera input
- Improved color recognition using machine learning
- Web-based interface version
- Performance benchmarking of solving algorithms
- Better integration between GUI and camera module

## 👤 Author

Kamil Miodowski

## 📄 License

This project uses the Rubik’s Cube Two-Phase Solver
based on the Kociemba algorithm.

Original implementation:
https://github.com/hkociemba/RubiksCube-TwophaseSolver

Licensed under GPLv3 (GNU General Public License v3.0).
