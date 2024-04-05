import cv2
import pytesseract
import numpy as np

def remove_text(image_path, threshold=50):
    """
    This function removes text from an image. It will first use OCR to detect the text regions and then inpaint them.
    :param image_path: The path to the input image
    :param threshold: The confidence threshold for OCR (default is 50)
    :return: The inpainted image
    """
    # Load the image
    img = cv2.imread(image_path)

    # Apply OCR to get the text regions
    text = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    # Initialize dst as a copy of the original image
    dst = img.copy()

    # Get the bounding boxes for the text regions
    n_boxes = len(text['text'])
    for i in range(n_boxes):
        if int(text['conf'][i]) < threshold:  # Confidence threshold
            continue
        (x, y, w, h) = (text['left'][i], text['top'][i], text['width'][i], text['height'][i])

        # Create a mask for the text region
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

        # Inpaint the text region
        dst = cv2.inpaint(dst, mask, 3, cv2.INPAINT_TELEA)

    return dst
