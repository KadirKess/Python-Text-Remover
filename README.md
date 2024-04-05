# Text Remover

Text Remover is a Python application that uses Optical Character Recognition (OCR) to detect and remove text from images. It provides a graphical user interface (GUI) for easy usage.

## Features

- Load an image (JPEG, PNG, WebP formats are supported)
- Set a confidence threshold for OCR text detection
- Remove detected text from the image
- Save the processed image

## Dependencies

The following Python packages are required to run the application:

- opencv-python
- pytesseract
- PyQt5
- numpy

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/KadirKess/Python-Text-Remover.git
   ```
2. Navigate to the project directory:
   ```
   cd Python-Text-Remover
   ```
3. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```
   or
   ```
   python3 main.py
   ```
2. Click on "Select Image" to choose an image.
3. Adjust the "Confidence Threshold" if needed.
4. Click on "Remove Text" to process the image.
5. Click on "Save Image" to save the processed image.
6. Click on "Close" to exit the application.

## How it works

The Text Remover application uses a combination of OpenCV and Pytesseract to detect and remove text from images. Here's a detailed breakdown of the process:

1. **Image Loading**: The script loads the image using OpenCV's `imread` function. This function reads the image from the specified file path and returns it in an array format that can be processed by the application.

2. **OCR Processing**: The loaded image is then processed using Pytesseract, an Optical Character Recognition (OCR) tool for Python. Pytesseract uses the Tesseract engine to detect and recognize text within the image. The `image_to_data` function is used, which returns the recognized text along with its bounding box coordinates and a confidence score.

3. **Text Region Identification**: The script then iterates over the detected text regions. If the confidence score of a text region is below the specified threshold, it is skipped. This is done to avoid removing regions that are not text. Otherwise, the bounding box coordinates of the text region are used to create a mask.

4. **Mask Creation**: A mask is a binary image where the pixels corresponding to the text region are set to 1 (or true), and all other pixels are set to 0 (or false). This mask is used to isolate the text region for further processing.

5. **Inpainting**: The masked region (i.e., the text region) is then inpainted using OpenCV's `inpaint` function. Inpainting is a process where the selected region in an image is filled with information extrapolated from the surrounding areas. In this case, it is used to fill the text region with similar colors and patterns from the rest of the image, effectively removing the text.

6. **Iterative Process**: This process is repeated for all detected text regions in the image, resulting in an image where the text has been removed.

## Project Structure

```
.
├── main.py
├── requirements.txt
└── src
    ├── gui.py
    └── ocr.py
```

- `main.py`: The entry point of the application.
- `src/gui.py`: The module that contains the GUI of the application.
- `src/ocr.py`: The module that contains the OCR functionality.
- `requirements.txt`: The list of Python packages required to run the application.
