import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QToolBar, QScrollArea, QLabel, QSizePolicy
)
from PySide6.QtGui import QPixmap, QAction, Qt, QPalette, QColor, QPainter, QFont
from PySide6.QtCore import QSize, QRectF

class ImageViewerWidget(QWidget):
    """
    A custom PySide6 widget for viewing images with zoom and fit-to-window functionality.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Image Viewer")
        self._image_path = None
        self._original_pixmap = QPixmap()
        self._current_pixmap = QPixmap()
        self._scale_factor = 1.0
        self._zoom_step = 0.1  # How much to zoom in/out each step
        self._min_scale_factor = 0.1
        self._max_scale_factor = 5.0

        self._init_ui()

    def _init_ui(self):
        """Initializes the user interface components of the widget."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # Remove margins for a snug fit
        main_layout.setSpacing(0) # Remove spacing between toolbar and scroll area

        # 1. Create ToolBar
        self.toolbar = QToolBar("Image Tools")
        self.toolbar.setIconSize(QSize(24, 24)) # Set icon size for better appearance

        # Zoom In Action
        self.zoom_in_action = QAction("Zoom In", self)
        self.zoom_in_action.setToolTip("Zoom in on the image (Ctrl++)")
        self.zoom_in_action.setShortcut("Ctrl++")
        self.zoom_in_action.triggered.connect(self.zoom_in)
        self.toolbar.addAction(self.zoom_in_action)

        # Zoom Out Action
        self.zoom_out_action = QAction("Zoom Out", self)
        self.zoom_out_action.setToolTip("Zoom out from the image (Ctrl+-)")
        self.zoom_out_action.setShortcut("Ctrl+-")
        self.zoom_out_action.triggered.connect(self.zoom_out)
        self.toolbar.addAction(self.zoom_out_action)

        # Fit Window Action
        self.fit_window_action = QAction("Fit Window", self)
        self.fit_window_action.setToolTip("Fit image to window (Ctrl+F)")
        self.fit_window_action.setShortcut("Ctrl+F")
        self.fit_window_action.triggered.connect(self.fit_to_window)
        self.toolbar.addAction(self.fit_window_action)

        main_layout.addWidget(self.toolbar)

        # 2. Create Image Viewer (Scroll Area with QLabel)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True) # Allow the widget inside to resize
        self.scroll_area.setAlignment(Qt.AlignCenter) # Center content when it's smaller

        # Set background color for the scroll area
        palette = self.scroll_area.palette()
        palette.setColor(QPalette.Window, QColor(Qt.darkGray))
        self.scroll_area.setPalette(palette)
        self.scroll_area.setAutoFillBackground(True) # Enable auto-fill for background

        self.image_label = QLabel()
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored) # Let scroll area manage size
        self.image_label.setScaledContents(False) # Important: we will scale QPixmap manually

        # Set background color for the image label (when no image is loaded or image doesn't fill)
        label_palette = self.image_label.palette()
        label_palette.setColor(QPalette.Window, QColor(Qt.darkGray))
        self.image_label.setPalette(label_palette)
        self.image_label.setAutoFillBackground(True) # Enable auto-fill for background


        self.scroll_area.setWidget(self.image_label)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

    def load_image(self, image_path: str):
        """
        Loads an image from the specified path into the viewer.

        Args:
            image_path (str): The file path to the image.
        """
        self._image_path = image_path
        self._original_pixmap = QPixmap(image_path)

        if self._original_pixmap.isNull():
            print(f"Error: Could not load image from {image_path}")
            self.image_label.setText("Failed to load image.")
            self.image_label.setAlignment(Qt.AlignCenter)
            self._current_pixmap = QPixmap() # Clear current pixmap
            self._scale_factor = 1.0
            self._update_actions_state(False)
        else:
            self.image_label.clear() # Clear any previous text
            self._scale_factor = 1.0 # Reset scale factor on new image load
            self.fit_to_window() # Fit the new image to the window initially
            self._update_actions_state(True)

    def _update_image_display(self):
        """
        Scales the original pixmap by the current scale factor and updates the QLabel.
        """
        if not self._original_pixmap.isNull():
            # Calculate the new size based on the original size and scale factor
            new_width = int(self._original_pixmap.width() * self._scale_factor)
            new_height = int(self._original_pixmap.height() * self._scale_factor)

            # Scale the pixmap while maintaining aspect ratio
            self._current_pixmap = self._original_pixmap.scaled(
                new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.image_label.setPixmap(self._current_pixmap)
            # Set fixed size for the label so the scroll area can manage scrolling
            self.image_label.setFixedSize(self._current_pixmap.size())
        else:
            self.image_label.clear()
            self.image_label.setFixedSize(0, 0) # Collapse label if no image

        self._update_actions_state(not self._original_pixmap.isNull())


    def zoom_in(self):
        """Zooms in on the image."""
        if self._original_pixmap.isNull():
            return

        new_scale = self._scale_factor + self._zoom_step
        if new_scale > self._max_scale_factor:
            new_scale = self._max_scale_factor

        if new_scale != self._scale_factor:
            self._scale_factor = new_scale
            self._update_image_display()

    def zoom_out(self):
        """Zooms out from the image."""
        if self._original_pixmap.isNull():
            return

        new_scale = self._scale_factor - self._zoom_step
        if new_scale < self._min_scale_factor:
            new_scale = self._min_scale_factor

        if new_scale != self._scale_factor:
            self._scale_factor = new_scale
            self._update_image_display()

    def fit_to_window(self):
        """Fits the image to the current size of the scroll area's viewport."""
        if self._original_pixmap.isNull():
            return

        # Get the current size of the scroll area's viewport
        viewport_size = self.scroll_area.viewport().size()
        image_size = self._original_pixmap.size()

        if image_size.isEmpty() or viewport_size.isEmpty():
            self._scale_factor = 1.0 # Default if sizes are invalid
            self._update_image_display()
            return

        # Calculate scale factors for width and height
        width_scale = viewport_size.width() / image_size.width()
        height_scale = viewport_size.height() / image_size.height()

        # Use the minimum of the two to ensure the entire image fits
        self._scale_factor = min(width_scale, height_scale)

        # Ensure scale factor is within limits
        if self._scale_factor < self._min_scale_factor:
            self._scale_factor = self._min_scale_factor
        elif self._scale_factor > self._max_scale_factor:
            self._scale_factor = self._max_scale_factor

        self._update_image_display()

    def resizeEvent(self, event):
        """
        Overrides the resize event to re-fit the image to the window if it was
        previously in 'fit to window' mode, or simply update the display.
        """
        super().resizeEvent(event)
        # If the image is currently smaller than the viewport, re-center it.
        # Otherwise, just ensure the scrollbars adjust to the new window size.
        # The QScrollArea handles scrollbar visibility automatically.
        # We just need to ensure the QLabel's size is correct.
        self._update_image_display()


    def _update_actions_state(self, enabled: bool):
        """Enables or disables toolbar actions based on whether an image is loaded."""
        self.zoom_in_action.setEnabled(enabled)
        self.zoom_out_action.setEnabled(enabled)
        self.fit_window_action.setEnabled(enabled)


class MainWindow(QMainWindow):
    """
    A simple main window to demonstrate the ImageViewerWidget.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Image Viewer Demo")
        self.setGeometry(100, 100, 800, 600) # Initial window size

        self.image_viewer = ImageViewerWidget(self)
        self.setCentralWidget(self.image_viewer)

        # Load a placeholder image for demonstration
        # In a real app, you would prompt the user to select an image or load from a path.
        # Create a simple dummy pixmap if no file exists for testing
        dummy_pixmap = QPixmap(200, 150)
        dummy_pixmap.fill(Qt.blue)
        painter = QPainter(dummy_pixmap) # Corrected: QPainter from QtGui
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 20)) # Corrected: QFont from QtGui
        painter.drawText(dummy_pixmap.rect(), Qt.AlignCenter, "Placeholder Image")
        painter.end()

        # Save the dummy pixmap to a temporary file
        temp_image_path = "temp_placeholder_image.png"
        dummy_pixmap.save(temp_image_path)

        self.image_viewer.load_image(temp_image_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
