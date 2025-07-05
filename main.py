from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QFrame, QSizePolicy, QMenuBar
)
from PySide6.QtCore import Qt, Slot
import os

from AppWidgets.MiniWidgets import create_card_frame
from AppWidgets.ImageGrid import ImageGridWindow
from AppWidgets.ImageViewer import ImageViewer

DATA_DIR = "data/images"

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My PySide6 App")

        # Central widget to hold our main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main vertical layout for the entire application
        self.main_v_layout = QVBoxLayout(self.central_widget)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0) # No extra margin on the central widget
        self.main_v_layout.setSpacing(0) # No extra spacing between main sections

        self.setup_ui()

    def setup_ui(self):
        # --- 1. Menu Bar (Red Color) ---
        # QMenuBar is typically part of QMainWindow, not a separate widget in a layout
        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet("background-color: red; color: white;")

        # app_name_label = QLabel("AppName", self.menu_bar)
        # app_name_label.setStyleSheet("padding: 5px; font-weight: bold; font-size: 16px;") # Add padding for spacing
        # You'd typically use QActions for menu items, but for simple buttons in the menubar, QLabel and QWidget can be styled.
        # However, for true menu functionality (dropdowns, shortcuts), QAction is the way.
        # For simplicity, let's just make "menu" items as actions
        view_list_action = self.menu_bar.addAction("Menu1")
        download_report_action = self.menu_bar.addAction("Menu2")

        # Align actions to the right (QMenuBar handles this automatically for actions)
        # For a more custom layout within the menu bar, you'd embed a QWidget and use a QHBoxLayout within it.
        # Example for right alignment of buttons in menubar (more complex but flexible):
        # right_menu_widget = QWidget(self.menu_bar)
        # right_menu_layout = QHBoxLayout(right_menu_widget)
        # right_menu_layout.setContentsMargins(0,0,0,0)
        # right_menu_layout.addStretch(1) # Pushes items to the right
        # right_menu_layout.addWidget(QPushButton("View List"))
        # right_menu_layout.addWidget(QPushButton("Download Report"))
        # self.menu_bar.setCornerWidget(right_menu_widget, Qt.TopRightCorner)


        # --- Main Content Area ---
        # This will contain the dropdown row and the 3-column row
        main_content_container = QWidget()
        main_content_layout = QVBoxLayout(main_content_container)
        main_content_layout.setContentsMargins(4, 4, 4, 4) # Padding for main content
        main_content_layout.setSpacing(4) # Spacing between rows

        # --- 2.1. First Row: 3 Dropdowns Horizontally (Max 60px height) ---
        dropdown_frame = create_card_frame(color="rgb(255,255,255)")
        dropdown_layout = QHBoxLayout(dropdown_frame)
        dropdown_layout.setContentsMargins(4, 4, 4, 4) # Padding within the card
        dropdown_layout.setSpacing(4) # Spacing between dropdowns

        # Set fixed height for the dropdown frame
        dropdown_frame.setFixedHeight(60)
        dropdown_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Example Dropdowns
        dropdown1 = QComboBox()
        dropdown1.setGeometry(0,0,40,100)
        options = os.listdir(DATA_DIR)
        dropdown1.addItems(list(options))
        dropdown1.setPlaceholderText("Select 1")
        dropdown1.setStyleSheet("background-color:rgb(255,255,255);color:rgb(23,23,23)")
        dropdown1.currentTextChanged.connect(self.setGridView)

        # dropdown2 = QComboBox()
        # dropdown2.addItems(["Option A", "Option B"])
        # dropdown2.setPlaceholderText("Select 2")

        # dropdown3 = QComboBox()
        # dropdown3.addItems(["Item X", "Item Y"])
        # dropdown3.setPlaceholderText("Select 3")

        dropdown_layout.addWidget(dropdown1)
        # dropdown_layout.addWidget(dropdown2)
        # dropdown_layout.addWidget(dropdown3)

        main_content_layout.addWidget(dropdown_frame)


        # --- 2.2. Second Row: 3 Columns ---
        columns_frame = create_card_frame()
        columns_layout = QHBoxLayout(columns_frame)
        columns_layout.setContentsMargins(4, 4, 4, 4) # Padding within the card
        columns_layout.setSpacing(4) # Spacing between columns

        # Column 1 (40% screen width)
        col1_frame = create_card_frame(color="rgb(255,255,255)")
        col1_layout = QVBoxLayout(col1_frame)
        col1_layout.addWidget(QLabel("Column 1 (40%)"))
        self.gridImage = self.setGridView(options[0])
        col1_layout.addWidget(self.gridImage)
       
        col1_layout.addStretch(1) # Push content to top

        # Column 2 (20% screen width or max 250px width)
        col2_frame = create_card_frame(color="rgb(255,255,255)")
        col2_layout = QVBoxLayout(col2_frame)
        col2_layout.addWidget(QLabel("Column 2 (20% or 250px max)"))
        col2_layout.addStretch(1)

        # Column 3 (Rest of the width, 2 rows)
        col3_frame = create_card_frame()
        col3_layout = QVBoxLayout(col3_frame)
        col3_layout.setContentsMargins(4, 4, 4, 4) # Padding within this sub-card
        col3_layout.setSpacing(4) # Spacing between rows in col3

        # Column 3 - Row 1 (Thumbnails - 50px height)
        col3_row1_frame = create_card_frame(color="rgb(255,255,255)")
        col3_row1_layout = QVBoxLayout(col3_row1_frame)
        col3_row1_layout.addWidget(QLabel("Thumbnails (50px)"))
        col3_row1_layout.addStretch(1)
        col3_row1_frame.setFixedHeight(50)
        col3_row1_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Column 3 - Row 2 (Takes the rest of the height)
        col3_row2_frame = create_card_frame(color="rgb(255,255,255)")
        col3_row2_layout = QVBoxLayout(col3_row2_frame)
        col3_row2_layout.addWidget(QLabel("Col 3 - Row 2 (Rest)"))
        self.patchImg = ImageViewer(None)
        col3_row2_layout.addWidget(self.patchImg)
        col3_row2_layout.addStretch(1)


        col3_layout.addWidget(col3_row1_frame)
        col3_layout.addWidget(col3_row2_frame)


        # Add columns to the main columns layout
        columns_layout.addWidget(col1_frame, 40) # Stretch factor 40 for 40%
        columns_layout.addWidget(col2_frame, 20) # Stretch factor 20 for 20%
        columns_layout.addWidget(col3_frame, 40) # Stretch factor 40 for the rest

        # Set fixed width for column 2, overriding stretch factor if it goes below 250px
        col2_frame.setMinimumWidth(250)


        main_content_layout.addWidget(columns_frame)

        self.main_v_layout.addWidget(main_content_container)

    def setGridView(self, value):
        print("{} selected".format(value))
        patches = [os.path.join(DATA_DIR,value,"patches",i) for i in os.listdir(os.path.join(DATA_DIR,value,"patches"))]
        print(len(patches))
        gridImage = ImageGridWindow(patches)
        gridImage.patch_clicked.connect(self.setPatchImage)
        return gridImage
    
    @Slot()
    def setPatchImage(self,image_path):
        self.patchImg.setImage(image_path)
        print(f"Patch image set to: {image_path}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyApp()
    window.resize(1000, 700) # Initial size for demonstration
    window.show()
    sys.exit(app.exec())