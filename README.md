# OnlyFace™ - Face capture and randomly select Project

## Overview

This project captures faces from a webcam feed, detects them using `dlib`, and assigns a unique ID to each face. Detected faces are saved as images in the `images` directory then randomly select only one.

## Control

- Press `q` to quit OnlyFace™.
- Press `c` to clear the captured faces list.
- Press `r` to randomly select one of the captured faces

## Requirements

- Python 3.x
- `opencv-python==4.10.0.84`
- `dlib==19.24.5`
- `numpy==2.0.1`
- `Pillolw==10.4.0`

To install the required packages, run:

```bash
pip install -r requirements.txt
```
## Usage

To start, run the following command:

```bash
python Onlyface.py
```

Captured face images will be saved in the `images` directory with unique IDs (e.g., `face_1.jpg`, `face_2.jpg`). The `r` key allows you to randomly select one of these images.

**Note**: All saved images in the `images` directory will be deleted when clearing captured faces list or quit the program.
