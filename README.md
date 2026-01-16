# Virtual Shirt Tracking

A computer vision application that overlays virtual shirts on people in video using pose detection.

## Overview

This project uses pose detection to identify shoulder landmarks on a person and dynamically overlay different shirt designs in real-time. The application allows users to browse and select from a collection of shirts using hand gestures.

## Features

- **Real-time Pose Detection**: Uses MediaPipe pose detection to identify body landmarks
- **Virtual Shirt Overlay**: Dynamically overlays shirts on the detected person based on shoulder position and width
- **Interactive Shirt Selection**: Browse through different shirt designs using hand gesture controls
- **Responsive Sizing**: Automatically scales and positions shirts based on detected shoulder width

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- cvzone
- MediaPipe

## Installation

1. Clone or download this project
2. Install required dependencies:
```bash
pip install opencv-python cvzone mediapipe
```

## Project Structure

```
Virtual_shirttracking/
├── shirt.py              # Main application script
├── README.md            # This file
└── Resources/
    ├── Shirts/          # Folder containing shirt image files
    ├── Videos/          # Folder containing video files for processing
    └── button.png       # Button images for UI controls
```

## Usage

1. Place your shirt images in the `Resources/Shirts/` folder
2. Place your video file in the `Resources/Videos/` folder (default: `1.mp4`)
3. Run the application:
```bash
python shirt.py
```

## How It Works

- The application reads a video file and processes each frame
- Pose detection identifies key body landmarks, specifically the shoulders (landmarks 11 and 12)
- Shirts are scaled proportionally based on the detected shoulder width
- Users can navigate between shirt designs using hand gestures detected in the video

## Controls

- **Left Hand Gesture**: Select previous shirt (left button area)
- **Right Hand Gesture**: Select next shirt (right button area)

## Notes

- Ensure video files are properly placed in `Resources/Videos/`
- Shirt images should be in PNG format with transparency for best results
- The application uses specific ratio adjustments for proper shirt alignment

## Author

Created for virtual clothing try-on demonstration

## License

Open for educational and personal use
