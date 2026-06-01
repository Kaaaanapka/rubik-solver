# Rubik Cube Solver App

A desktop application for interacting with, analyzing, and solving the Rubik’s Cube using manual input, camera-based color detection, and an optimal solving algorithm.

---

## 🚀 Features

### 🎮 GUI Interface
- Manual input of Rubik’s Cube colors via visual cube layout
- Reset functionality
- Controls for solving and session management

### 📷 Camera-Based Color Detection
- Integration with external camera sources (e.g. DroidCam)
- Region of Interest (ROI) detection for extracting cube face colors (`roi.py`)
- Detection of 3x3 cube stickers from live video stream
- Planned improvement: full automatic cube reconstruction

### 🔀 Scramble Generator
- Generates official-style Rubik’s Cube scrambles
- Uses Singmaster notation (R, U, R', U', etc.)

### ⏱ Timer & Move Tracking
- Speedcubing timer system
- Manual move input tracking (notation-based)
- Stores solve sessions and move history

### 💾 Data Storage
- Saves solve sessions
- Stores move sequences for later analysis
- Supports export to structured formats (e.g. Excel / database)

---

## 🧠 Core Solving Engine

This project uses the **Kociemba Two-Phase Algorithm** for solving the Rubik’s Cube in optimal or near-optimal solutions (typically ~19 moves).

The implementation is based on:

https://github.com/hkociemba/RubiksCube-TwophaseSolver

This solver is widely used in professional cube-solving systems and provides efficient optimal solutions.

---

## 🛠 Tech Stack

- Python
- OpenCV (computer vision)
- Django / REST API (backend logic)
- GUI framework (Tkinter / PyQt)
- NumPy / Pandas
- RubikTwoPhase (Kociemba solver)

---

## 📁 Project Structure

src/
├── manage.py
├── client/
│ └── gui.py
├── roi.py
├── (additional modules: scramble, timer, storage, etc.)

## ▶️ How to Run

### Backend
python manage.py runserver

### GUI
python client/gui.py

📌 Future Improvements
- Full automatic cube reconstruction from camera input
- Improved color recognition using machine learning
- Web-based interface version
- Performance benchmarking of solving algorithms
- Better integration between GUI and camera module

👤 Author

Kamil Miodowski

📄 License

This project uses the Rubik’s Cube Two-Phase Solver
based on the Kociemba algorithm.

Original implementation:
https://github.com/hkociemba/RubiksCube-TwophaseSolver

Licensed under GPLv3 (GNU General Public License v3.0).
