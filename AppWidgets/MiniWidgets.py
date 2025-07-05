
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QFrame, QSizePolicy, QMenuBar
)
from PySide6.QtCore import Qt, Signal, Slot


def create_card_frame(color="rgb(235,235,235)"):
        """Helper to create a QFrame with the 'card' styling."""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Plain)
        frame.setLineWidth(0)
        frame.setStyleSheet("QFrame { border: 1px solid gray; background-color:"+color+" ; }") # Background for visibility
        return frame

class ClickableLabel(QLabel):
    """
    A QLabel subclass that emits a clicked signal when clicked.
    """
    widgetClicked = Signal()

    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        # Make the label appear clickable by changing the cursor
        self.setCursor(Qt.PointingHandCursor)
        if text is not None and text!="":
             self.setText(text)

    def mousePressEvent(self, event):
        """
        Reimplements mousePressEvent to emit the clicked signal.
        """
        if event.button() == Qt.LeftButton:
            self.widgetClicked.emit()
        super().mousePressEvent(event) # Call the base class implementation    