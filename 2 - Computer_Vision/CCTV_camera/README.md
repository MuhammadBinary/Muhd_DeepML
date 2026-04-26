# 📹 Advanced CCTV Camera

## Project Overview

This project implements a real-time motion detection and alerts. Designed for basic surveillance, it leverages computer vision techniques to identify movement within the camera's field of view and trigger actions such as SAVES frames and generating audio alerts.

## ✨ Features

*   **Real-time Motion Detection:** Continuously monitors video feed for changes between frames.
*   **Visual Bounding Boxes:** Draws rectangles around detected motion for easy identification.
*   **Frame Saving on Motion:** Automatically saves images when significant motion is detected.
*   **Audio Alerts:** Triggers a beep sound and speaks a greeting upon startup (Windows-specific).

## ⚙️ Technologies Used

*   **Python:** The core programming language.
*   **OpenCV (`cv2`):** For video capture, frame processing, and motion detection.
*   **NumPy:** For numerical operations (implicitly used by OpenCV).
*   **`winsound` (Windows-only):** For playing system sounds.
*   **`pyttsx3` (Windows-only):** For text-to-speech functionality.
*   **`datetime`:** For timestamping events.

## 🚀 How It Works

1.  **Video Stream Capture:** The system captures video from the default webcam.
2.  **Frame Differencing:** It compares consecutive frames to detect changes, indicating movement.
3.  **Grayscale & Blur:** Frames are converted to grayscale and blurred to reduce noise and highlight significant motion.
4.  **Thresholding & Dilation:** Thresholding is applied to create a binary image of motion, which is then dilated to enhance motion areas.
5.  **Contour Detection:** Contours are found around the dilated motion areas.
6.  **Motion Filtering:** Small contours (insignificant movements) are filtered out.
7.  **Alerts & Saving:** If significant motion is detected, a bounding box is drawn, a frame is saved, and an audio alert is triggered (on Windows).

## 📊 Project Structure

```
CCTV_camera/
└── CCTV_camera.py   # Main script for the advanced CCTV camera
```

## 💻 Installation & Usage

### Prerequisites

*   Python 3.x
*   Webcam

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MuhammadBinary/Muhd_AI_repo.git
    cd Muhd_AI_repo/Computer_Vision/CCTV_camera
    ```

2.  **Install dependencies:**
    ```bash
    pip install opencv-python numpy pyttsx3
    ```
    *Note: `winsound` is a built-in Windows module and does not require installation. `pyttsx3` might require additional system-level speech packages depending on your OS.*

### Running the Application

```bash
python CCTV_camera.py
```

Press `q` to quit the application.

## ⚠️ Platform-Specific Notes

*   The `winsound` and `pyttsx3` modules are primarily designed for Windows environments. While `pyttsx3` can be configured for other OS (e.g., `espeak` on Linux), `winsound` functionality will not be available on non-Windows systems. The core motion detection and frame saving will still function.

## 💡 Future Enhancements

*   **Cross-platform Audio Alerts:** Implement platform-agnostic audio alerts.
*   **Notification System:** Integrate email or push notifications for motion alerts.
*   **Recording Functionality:** Add continuous video recording with motion-triggered segments.
*   **Object Recognition:** Integrate object detection to identify what caused the motion.
*   **Web Interface:** Develop a web-based interface for remote monitoring and control.
