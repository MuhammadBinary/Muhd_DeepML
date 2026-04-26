# 👤 Face Recognition Attendance System

## Project Overview

This project develops an automated attendance system using real-time face recognition. It identifies individuals from a live webcam feed and marks their attendance in a CSV file, providing a modern and efficient alternative to traditional attendance methods.

## ✨ Features

*   **Real-time Face Detection:** Detects faces in a live video stream.
*   **Face Recognition:** Identifies known individuals by comparing their facial encodings with a database of registered faces.
*   **Automated Attendance Marking:** Records the name and timestamp of recognized individuals in a `Attendance.csv` file.
*   **Visual Feedback:** Displays bounding boxes and names on recognized faces in the video feed.
*   **Scalable:** Easily add new faces to the attendance system by placing their images in the `ImagesAttendance` folder.

## ⚙️ Technologies Used

*   **Python:** The core programming language.
*   **OpenCV (`cv2`):** For real-time video capture and image processing.
*   **`face_recognition` library:** A powerful library for face detection and recognition, built upon `dlib`.
*   **NumPy:** For numerical operations and array manipulation.
*   **`datetime`:** For timestamping attendance records.
*   **`os`:** For interacting with the operating system, such as listing image files.

## 🚀 How It Works

1.  **Load Known Faces:** The system loads images of authorized individuals from the `ImagesAttendance` folder and computes their unique facial encodings.
2.  **Video Stream Capture:** A live video feed is captured from the webcam.
3.  **Face Detection & Encoding (Current Frame):** For each frame, faces are detected, and their facial encodings are computed.
4.  **Face Comparison:** The encodings of faces in the current frame are compared against the encodings of known faces.
5.  **Identification & Attendance:** If a match is found, the individual is identified, their name is displayed on the video feed, and their attendance is marked in the `Attendance.csv` file with a timestamp.

## 📊 Project Structure

```
Face-Recognition/
├── main.py                  # Main script for the face recognition attendance system
├── Attendance.csv           # Stores attendance records (created/updated by the script)
├── ImagesAttendance/        # Folder containing images of known individuals
│   ├── Elon Musk.jpg
│   ├── Haruna.jpg
│   ├── Mark Zugerburg.jpg
│   ├── Muckhtar.jpg
│   └── Muhd.jpg
└── ... (other image files)
```

## 💻 Installation & Usage

### Prerequisites

*   Python 3.x
*   Webcam

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MuhammadBinary/Muhd_AI_repo.git
    cd Muhd_AI_repo/Computer_Vision/Face-Recognition
    ```

2.  **Install dependencies:**
    ```bash
    pip install opencv-python numpy face_recognition
    ```
    *Note: The `face_recognition` library might require `dlib` to be installed first, which can sometimes be complex. Refer to `dlib` installation guides if you encounter issues.*

### Adding New Faces

To add a new person to the attendance system, simply place a clear image of their face (e.g., `NewPerson.jpg`) into the `ImagesAttendance` folder. The system will automatically detect and encode this face on the next run.

### Running the Application

```bash
python main.py
```

Once running, a window will display your webcam feed. When a known face is detected, its name will appear, and attendance will be logged.

## 💡 Future Enhancements

*   **User Interface:** Develop a graphical user interface for managing known faces and viewing attendance records.
*   **Database Integration:** Replace CSV with a more robust database (e.g., SQLite, MySQL) for storing attendance data.
*   **Liveness Detection:** Implement techniques to prevent spoofing (e.g., using photos or videos).
*   **Cloud Integration:** Store face encodings and attendance records in a cloud service.
*   **Reporting Features:** Generate daily/weekly attendance reports.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or new features, please feel free to fork the repository and submit a pull request.
