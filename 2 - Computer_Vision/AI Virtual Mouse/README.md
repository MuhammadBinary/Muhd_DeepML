# 🖱️ AI Virtual Mouse

## Project Overview

The AI Virtual Mouse is an innovative computer vision project that allows users to control their mouse cursor and perform click actions using hand gestures. This touchless interface enhances accessibility and provides a futuristic way to interact with your computer, leveraging real-time hand tracking and gesture recognition.

## ✨ Features

*   **Real-time Hand Tracking:** Utilizes MediaPipe to accurately detect and track hand landmarks.
*   **Gesture-based Control:** Move the cursor by moving your index finger and perform clicks by bringing your index and middle fingers together.
*   **Smooth Cursor Movement:** Implements a smoothening algorithm for precise and fluid cursor control.
*   **Customizable Frame Rate:** Displays the frame rate for performance monitoring.
*   **Screen Adaptation:** Automatically adapts to your screen resolution for seamless interaction.

## ⚙️ Technologies Used

*   **Python:** The core programming language.
*   **OpenCV (`cv2`):** For real-time video capture and image processing.
*   **MediaPipe:** For robust and accurate hand landmark detection.
*   **NumPy:** For numerical operations, especially coordinate interpolation.
*   **`autopy`:** For programmatic control of the mouse cursor.

## 🚀 How It Works

1.  **Video Stream Capture:** The webcam captures a live video feed.
2.  **Hand Landmark Detection:** MediaPipe processes each frame to identify key points (landmarks) on the hand.
3.  **Finger State Analysis:** The system determines which fingers are extended (up) based on landmark positions.
4.  **Cursor Movement (Moving Mode):** When only the index finger is up, its tip coordinates are mapped and interpolated to the screen resolution, controlling the mouse cursor.
5.  **Click Action (Clicking Mode):** When both the index and middle fingers are up and brought close together, a click event is triggered.
6.  **Visual Feedback:** Rectangles and circles are drawn on the video feed to indicate the active area and finger positions.

## 📊 Project Structure

```
AI Virtual Mouse/
├── Virtual Mouse.py         # Main script for the AI Virtual Mouse
├── HandTrackingModule.py    # Helper module for hand detection and tracking
└── ADcam.py                 # (Optional) Script for Android camera integration
```

## 💻 Installation & Usage

### Prerequisites

*   Python 3.x
*   Webcam

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MuhammadBinary/Muhd_AI_repo.git
    cd Muhd_AI_repo/Computer_Vision/AI\ Virtual\ Mouse
    ```

2.  **Install dependencies:**
    ```bash
    pip install opencv-python mediapipe numpy autopy
    ```

### Running the Application

```bash
python "Virtual Mouse.py"
```

Once running, a window will display your webcam feed. Move your index finger to control the mouse, and bring your index and middle fingers together to click.

## 💡 Future Enhancements

*   **Multi-gesture Support:** Implement more gestures for advanced controls (e.g., scroll, drag-and-drop).
*   **Customizable Gestures:** Allow users to define their own gestures.
*   **Performance Optimization:** Further optimize the code for lower latency and higher frame rates.
*   **User Interface:** Develop a simple GUI for configuration and settings.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or new features, please feel free to fork the repository and submit a pull request.
