# OnlyFace™ - Face capture and randomly select Project

## Overview

This project captures faces from a webcam feed, detects them using `dlib`, and assigns a unique ID to each face. Detected faces are saved as images in the `images` directory then randomly select only one.

## Control

press "q" to stop and quit Onlyface
press "c" to clear captured faces list
(WIP)press "r" to randomly select one of the capture faces

## Requirements

- Python 3.x
- `opencv-python==4.10.0.84`
- `dlib==19.24.5`
- `numpy==2.0.1`

To install the required packages, run:

```bash
pip install -r requirements.txt