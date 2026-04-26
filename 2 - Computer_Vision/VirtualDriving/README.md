# 🚗 Virtual Driving

## Project Overview

This project transforms your webcam into an interactive driving simulator, allowing you to control a virtual car using a physical steering wheel (or a red-colored object acting as one). By detecting the position of the steering wheel, the system translates physical movements into virtual driving commands (left, right, go, stop), offering an engaging and immersive experience for basic driving simulation. This is also one of the project that we play alot with i.e Me and My brother.

## ✨ Features

*   **Real-time Steering Detection:** Identifies and tracks a red-colored steering wheel in the webcam feed.
*   **Gesture-based Driving Controls:** Translates steering wheel position into virtual commands: turn left, turn right, accelerate (go), and brake (stop).
*   **Visual Feedback:** Displays control zones and the detected steering wheel position on the screen.
*   **`pyautogui` Integration:** Sends keyboard commands to control external applications or games.

## ⚙️ Technologies Used

*   **Python:** The core programming language.
*   **OpenCV (`cv2`):** For real-time video capture and image processing.
*   **`cvzone`:** A computer vision helper library for tasks like color filtering and contour detection.
*   **`cvzone.ColorModule`:** Specifically used for color detection and mask generation.
*   **`pyautogui`:** For programmatically controlling the keyboard (sending 'up', 'down', 'left', 'right' key presses).

## 🚀 How It Works

1.  **Video Stream Capture:** The webcam captures a live video feed.
2.  **Color-based Steering Detection:** The system uses `cvzone.ColorModule` to detect a specific red color range, identifying the steering wheel.
3.  **Contour Detection:** Contours are found around the detected red object to determine its shape and center.
4.  **Control Zone Mapping:** The video frame is divided into logical control zones (left, right, go, stop).
5.  **Command Translation:** Based on the steering wheel's center position within these zones, corresponding keyboard commands (`up`, `down`, `left`, `right`) are sent via `pyautogui`.

## 📊 Project Structure

```
VirtualDriving/
├── main.py                  # Main script for the virtual driving simulator
└── Resources/               # (Optional) Contains images or assets for the project
    └── steering2.jpg        # Example steering wheel image
```

## 💻 Installation & Usage

### Prerequisites

*   Python 3.x
*   Webcam
*   A physical steering wheel or a red-colored object to act as one.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MuhammadBinary/Muhd_AI_repo.git
    cd Muhd_AI_repo/Computer_Vision/VirtualDriving
    ```

2.  **Install dependencies:**
    ```bash
    pip install opencv-python cvzone pyautogui
    ```

### Running the Application

```bash
python main.py
```

**Instructions for Use:**

*   Ensure you have a red-colored steering wheel or object. The code is configured to detect a specific red HSV range.
*   Position yourself approximately 60cm from the webcam.
*   Ensure you have a white background for optimal detection.
*   The application will display a window with your webcam feed and control zones. Move your steering wheel to control the virtual car.

## 💡 Future Enhancements

*   **Customizable Color Detection:** Allow users to calibrate the color range for their steering wheel.
*   **Advanced Game Integration:** Develop a more direct integration with specific racing games or simulators.
*   **Feedback Mechanisms:** Add haptic or audio feedback for driving actions.
*   **Multi-object Detection:** Support for pedals (accelerator/brake) using additional color detection.
*   **Improved Smoothening:** Enhance cursor movement smoothening for more realistic control.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or new features, please feel free to fork the repository and submit a pull request.
