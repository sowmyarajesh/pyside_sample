from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy,
                                QLabel, QScrollArea, QFrame, QMessageBox)
from PySide6.QtGui import (QColorSpace, QGuiApplication,
                           QImageReader, QImageWriter, QKeySequence,
                           QPalette, QPainter, QPixmap)
from PySide6.QtCore import QDir, QStandardPaths, Qt, Slot, Signal, QFile


class ImageViewer(QMainWindow):
    image_clicked = Signal()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.image_label.setSizePolicy(QLabel.Ignored, QLabel.Ignored)
        self.image_label.setScaledContents(True)  # Important: allows QLabel to scale the image

        self.layout.addWidget(self.image_label)
    
    @Slot()
    def setImage(self, img_path):
        pix = QPixmap(img_path)
        if not pix.isNull():
            self.image_label.setPixmap(pix)
            self.image_label.adjustSize()
        else:
            QMessageBox.warning(self, "Image Load Error", f"Could not load image from {img_path}")
        