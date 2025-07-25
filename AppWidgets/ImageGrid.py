import sys
from PySide6.QtWidgets import (QApplication,QMainWindow, QWidget, QGridLayout, QLabel)
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtCore import Signal
from PySide6.QtCore import QSize

from AppWidgets.MiniWidgets import ClickableLabel
from AppWidgets.ImageViewer import ImageViewer
from assets.widgetStyles import highlight_image_label


class ImageGridWindow(QMainWindow):
    patch_clicked = Signal(str)

    def __init__(self, image_paths):
        super().__init__()
        self.setWindowTitle("Image Grid")

        central_widget = QWidget()
        grid_layout = QGridLayout(central_widget)
        central_widget.setStyleSheet("background-color:rgb(255,255,255);")

        if len(image_paths) != 16:
            print("Warning: Expected 16 image paths for a 4x4 grid.")
        else:
            row = 0
            col = 0
            for image_path in image_paths:
                print(image_path)
                image_label = ClickableLabel(self)
                image_label.setGeometry(0,0,150,150) ##XYWH

                pixmap = QPixmap(image_path)
                res = QSize(100,100) # Resize to 100x100 pixels
                pixmap = pixmap.scaled(res, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignCenter)
                needed_style= highlight_image_label(color="rgb(235,0,0)")
                if (row+col)%10 ==0:  ## THIS SECTION HAS TO BE CHANGED TO PREDICTION BASED
                    image_label.setStyleSheet(needed_style)
                # update lambda to map the path to this image click
                image_label.widgetClicked.connect(lambda path=image_path: (self.image_clicked(path), print(f"Image clicked: {path}")))

                grid_layout.addWidget(image_label, row, col)

                col += 1
                if col == 4:
                    col = 0
                    row += 1

        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)
    
    def image_clicked(self, image_path):
        self.patch_clicked.emit(image_path)

# Example usage
if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_paths = [f"image_{i}.png" for i in range(16)]  # Mock paths for illustration
    window = ImageGridWindow(image_paths)
    window.show()
    sys.exit(app.exec())
