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
        self.image=QLabel()
        self.setCentralWidget(self.central_widget)
        

    def paintEvent(self, event):
        painter = QPainter(self)        
        if not self.image.isNull():            
            # Calculate scaled image size keeping the aspect ratio
            scaled_image = self.image.pixmap().scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, 
                                                Qt.TransformationMode.SmoothTransformation)
            x_offset =(self.width() - scaled_image.width())//2
            y_offset = (self.height() - scaled_image.height()) // 2
            painter.drawImage(x_offset, y_offset, scaled_image)
            painter.end()
    
    @Slot()
    def setImage(self, img_path):
        pix = QPixmap(img_path)
        self.image.setPixmap(pix)
        