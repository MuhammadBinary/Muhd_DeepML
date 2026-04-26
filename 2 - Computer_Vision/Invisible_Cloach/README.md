# 🧙 Invisible Cloak

## Project Overview

Inspired by the magical invisibility cloak from popular fiction, this project shows a real-time computer vision application that makes a red-colored object (like a piece of cloth) appear invisible. By leveraging color detection and background subtraction techniques, the system creates an illusion where the background is visible through the red object, offering an engaging example of augmented reality using basic computer vision principles. And also a very fun project my small brother loves.

## ✨ Features

*   **Real-time Invisibility Effect:** Makes red objects disappear from the video feed in real-time.
*   **Background Capture:** Automatically captures the background before the invisibility effect begins.
*   **Color-based Detection:** Uses HSV color space to accurately detect red color.
*   **Morphological Operations:** Employs opening and dilation to refine the detected mask and reduce noise.

## ⚙️ Technologies Used

*   **Python:** The core programming language.
*   **OpenCV (`cv2`):** For video capture, image processing, color space conversion, and morphological operations.
*   **NumPy:** For numerical operations, especially array manipulation for masks.
*   **`time`:** For introducing delays during background capture.

## 🚀 How It Works

1.  **Background Calibration:** The system first captures several frames of the environment without the red object to establish a static background. This background will be used to replace the red object.
2.  **Video Stream Capture:** A live video feed is continuously captured from the webcam.
3.  **Color Detection (HSV):** Each frame is converted from BGR to HSV color space. Two ranges for red color are defined to cover the full spectrum of red hues.
4.  **Mask Creation:** A mask is generated to isolate all red pixels in the frame. Morphological operations (opening and dilation) are applied to this mask to remove small imperfections and smooth the edges.
5.  **Background Substitution:** The detected red areas in the current frame are replaced with the corresponding pixels from the pre-captured background image.
6.  **Final Output:** The modified frame, showing the 
invisible effect, is displayed.

## 📊 Project Structure

```
Invisible_Cloach/
└── Invisiablecloak.py       # Main script for the invisible cloak effect
```

## 💻 Installation & Usage

### Prerequisites

*   Python 3.x
*   Webcam
*   A red-colored object (e.g., a red cloth, scarf, or shirt)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MuhammadBinary/Muhd_AI_repo.git
    cd Muhd_AI_repo/Computer_Vision/Invisible_Cloach
    ```

2.  **Install dependencies:**
    ```bash
    pip install opencv-python numpy
    ```

### Running the Application

```bash
python Invisiablecloak.py
```

**Instructions for Use:**

1.  Run the script. The camera will capture the background for a few seconds. Ensure there is no red object in the frame during this calibration phase.
2.  After calibration, introduce your red-colored object into the frame. You will see the invisibility effect in action!
3.  Press `k` to quit the application.

## 💡 Future Enhancements

*   **Multiple Color Detection:** Extend the functionality to make objects of other colors invisible.
*   **Dynamic Background Update:** Implement a method to update the background dynamically, allowing for movement of the camera.
*   **Improved Masking:** Utilize more advanced segmentation techniques for smoother and more accurate invisibility effects.
*   **Interactive Controls:** Add controls for adjusting color detection thresholds in real-time.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or new features, please feel free to fork the repository and submit a pull request.
