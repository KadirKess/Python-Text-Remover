from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QSlider
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
from src.ocr import remove_text

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text Remover")
        self.setGeometry(100, 100, 600, 700)

        self.image_path = None
        self.output_image = None

        self.create_widgets()

    def create_widgets(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create two frames: one for buttons and one for the image

        # Button Frame: Below, 200x600
        self.buttons_frame = QWidget(central_widget)
        layout.addWidget(self.buttons_frame)

        # Image Canva: Up, 600x600, Gray Background
        self.image_label = QLabel(central_widget)
        self.image_label.setFixedSize(600, 600)
        self.image_label.setStyleSheet("background-color: gray;")
        layout.addWidget(self.image_label)

        # Add widgets for file selection, threshold input, and buttons
        self.file_button = QPushButton("Select Image", self.buttons_frame)
        self.file_button.clicked.connect(self.select_image)
        layout.addWidget(self.file_button)

        self.threshold_label = QLabel("Confidence Threshold (0-100):", self.buttons_frame)
        layout.addWidget(self.threshold_label)

        self.threshold_slider = QSlider(Qt.Horizontal, self.buttons_frame)
        self.threshold_slider.setRange(0, 100)
        self.threshold_slider.setValue(50)
        self.threshold_slider.valueChanged.connect(self.update_threshold_value)
        layout.addWidget(self.threshold_slider)

        self.process_button = QPushButton("Remove Text", self.buttons_frame)
        self.process_button.clicked.connect(self.process_image)
        self.process_button.setEnabled(False)
        layout.addWidget(self.process_button)

        self.save_button = QPushButton("Save Image", self.buttons_frame)
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button)

        self.close_button = QPushButton("Close", self.buttons_frame)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

    def select_image(self):
        # Open a file dialog to select an image
        filetypes = "JPEG Files (*.jpg);;PNG Files (*.png);;WebP Files (*.webp)"
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", filetypes)
        if self.image_path:
            self.process_button.setEnabled(True)
            self.display_image()
        else:
            self.process_button.setEnabled(False)

    def display_image(self):
        # Display the selected image in the GUI
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            scaled_pixmap = pixmap.scaled(600, int(pixmap.height() * (600 / pixmap.width())), Qt.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)

    def process_image(self):
        # Process the selected image using the specified threshold
        if self.image_path:
            threshold = self.threshold_slider.value()
            processed_image = remove_text(self.image_path, threshold)
            self.output_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            self.display_output_image()
            self.save_button.setEnabled(True)

    def display_output_image(self):
        # Display the processed image in the GUI
        output_image = QImage(self.output_image, self.output_image.shape[1], self.output_image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(output_image)
        scaled_pixmap = pixmap.scaled(600, int(pixmap.height() * (600 / pixmap.width())), Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)

    def save_image(self):
        # Save the processed image to a file
        if self.output_image is not None:
            filetypes = "JPEG Files (*.jpg);;PNG Files (*.png);;WebP Files (*.webp)"
            output_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", filetypes)
            cv2.imwrite(output_path, cv2.cvtColor(self.output_image, cv2.COLOR_RGB2BGR))

    def update_threshold_value(self, value):
        self.threshold_label.setText(str(value))