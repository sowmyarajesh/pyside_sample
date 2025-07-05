from PySide6.QtWidgets import (
     QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QFormLayout,
    QLabel, QPushButton, QComboBox, QFrame, QScrollArea,QSizePolicy
)

from PySide6.QtGui import QPixmap, QAction
from PySide6.QtGui import   QCursor
from PySide6.QtCore import Qt

from AppModules.AppData import AppData
from AppWidgets.ImageGrid import ImageGridWindow
from AppWidgets.ImageViewer import ImageViewer
from AppWidgets.MiniWidgets import create_card_frame, create_combo_box




class Page2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.appData = AppData()
        self.selected_plate = None
        self.selected_well = None
        self.selected_measurement = None
        self.selected_patch_path = None
        self.patch_path_list = []
        self.plateNames = self.appData.getPlateNames()
        total_recs = self.appData.getTotalRecords()
        self.dataset = self.appData.getDataByIndex(-1)
        if total_recs> 0:
            self.setSelectedPlate(self.plateNames[0])
        print("DEBUG::: Page2.__init__ ::: selected plate = {}".format(self.selected_plate))
        self.page_data = {
            "patch_name":"",
            "cell_count":0,
        }
        ## init base widgets
        self.patchImage = QLabel() #ImageViewer()
        self.patchImage.setGeometry(0,0,400,400)
        # self.patchImage.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Ignored)
        self.patchImage.setScaledContents(True)
        self.setWindowTitle("SCANN App/Page2")

        # Central widget to hold our main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main vertical layout for the entire application
        self.main_v_layout = QVBoxLayout(self.central_widget)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0) # No extra margin on the central widget
        self.main_v_layout.setSpacing(0) # No extra spacing between main sections

        self.setup_ui()

    def setup_ui(self):
    
        # --- Main Content Area ---
        # This will contain the dropdown row and the 3-column row
        main_content_container = QWidget()
        main_content_layout = QVBoxLayout(main_content_container)
        main_content_layout.setContentsMargins(4, 4, 4, 4) # Padding for main content
        main_content_layout.setSpacing(4) # Spacing between rows
        main_content_container.setStyleSheet("background-color:rgb(235,235,235);")

        # ---1. First Row: 3 Dropdowns Horizontally (Max 60px height) ---
        dropdown_frame = create_card_frame(color="rgb(255,255,255)")
        dropdown_layout = QHBoxLayout(dropdown_frame)
        dropdown_layout.setContentsMargins(4, 4, 4, 4) # Padding within the card
        dropdown_layout.setSpacing(4) # Spacing between dropdowns

        # Set fixed height for the dropdown frame
        dropdown_frame.setFixedHeight(60)
        dropdown_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Plates dropdown
        plates_dropdown = create_combo_box(self.plateNames, self.selected_plate)
        plates_dropdown.setPlaceholderText("Select Plate name")
        plates_dropdown.currentTextChanged.connect(self.setSelectedPlate)
        # Wells dropdown
        self.well_dropdown = create_combo_box(self.appData.getWellNames(self.selected_plate))
        self.well_dropdown.setPlaceholderText("Select Well Name")
        self.setSelectedWell(self.well_dropdown.currentText())
        self.well_dropdown.currentTextChanged.connect(self.setSelectedWell)
        # Measurement dropdown
        measurement_dropdown = create_combo_box(["001", "002", "003", "004"], "001")
        measurement_dropdown.setPlaceholderText("Select Measurement")
        self.setSelectedMeasurement(measurement_dropdown.currentText())
        measurement_dropdown.currentTextChanged.connect(self.setSelectedMeasurement)

        dropdown_layout.addWidget(plates_dropdown)
        dropdown_layout.addWidget(self.well_dropdown)
        dropdown_layout.addWidget(measurement_dropdown)

        main_content_layout.addWidget(dropdown_frame)


        # --- 2. Second Row: 3 Columns ---
        columns_frame = create_card_frame(color="rgb(235,235,235)")
        columns_layout = QHBoxLayout(columns_frame)
        columns_layout.setContentsMargins(4, 4, 4, 4) # Padding within the card
        columns_layout.setSpacing(4) # Spacing between columns

        # Column 1 (40% screen width) grid view of all patches
        col1_frame = create_card_frame(color="rgb(255,255,255)")
        col1_layout = QVBoxLayout(col1_frame)
        col1_layout.addStretch(1) # Push content to top
        
        if len(self.patch_path_list) > 0:
            self.setSelectedPatchPath(self.patch_path_list[0])
            self.patch_grid = ImageGridWindow(self.patch_path_list)
            self.patch_grid.patch_clicked.connect(self.setSelectedPatchPath)
        col1_layout.addWidget(self.patch_grid)
        col1_layout.addStretch(1)

        # Column 2 (20% screen width or max 250px width)
        col2_frame = create_card_frame(color="rgb(255,255,255)")
        col2_layout = QVBoxLayout(col2_frame)
        self.img_data = QFormLayout()
        self.img_data.addRow(QLabel("Selected Patch: "), QLabel(self.page_data["patch_name"]))
        self.img_data.addRow(QLabel("No. of Cells: "), QLabel(str(self.page_data["cell_count"])))
        self.img_data.addRow(QLabel("No. of Cells: "), QLabel(str(self.page_data["cell_count"])))
        col2_layout.addLayout(self.img_data)
        col2_layout.addStretch(1)

        # Column 3 (Rest of the width, 2 rows)
        col3_frame = create_card_frame()
        col3_layout = QVBoxLayout(col3_frame)
        col3_layout.setContentsMargins(4, 4, 4, 4) # Padding within this sub-card
        col3_layout.setSpacing(4) # Spacing between rows in col3

        # Column 3 - Row 1 (Thumbnails - 50px height)
        ## @TODO: Update the code to reflect the model results.
        col3_row1_frame = create_card_frame(color="rgb(255,255,255)")
        col3_row1_layout = QHBoxLayout(col3_row1_frame)
        col3_row1_layout.addWidget(self.updated_cellpicture())
        col3_row1_layout.addWidget(self.updated_cellpicture())
        col3_row1_layout.addStretch(1)
        col3_row1_frame.setFixedHeight(50)
        col3_row1_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Column 3 - Row 2 (Takes the rest of the height)
        col3_row2_frame = create_card_frame(color="rgb(255,255,255)")
        col3_row2_layout = QVBoxLayout(col3_row2_frame)
        col3_row2_layout.addWidget(self.patchImage)
        col3_row2_layout.addStretch(1)

        col3_layout.addWidget(col3_row1_frame)
        col3_layout.addWidget(col3_row2_frame)


        # Add columns to the main columns layout
        columns_layout.addWidget(col1_frame, 40) # Stretch factor 40 for 40%
        columns_layout.addWidget(col2_frame, 20) # Stretch factor 20 for 20%
        columns_layout.addWidget(col3_frame, 40) # Stretch factor 40 for the rest

        # Set fixed width for column 2, overriding stretch factor if it goes below 250px
        col2_frame.setMinimumWidth(200)
        col1_frame.setMinimumWidth(300)
        col3_frame.setMinimumWidth(500)

        main_content_layout.addWidget(columns_frame)

        self.main_v_layout.addWidget(main_content_container)

    def parsePatchName(self):
        if self.selected_patch_path is not None:
            _t = self.selected_patch_path.split("_")[-1]
            return f"Patch-{_t.split('.')[0]}"
        return ""
    
    def setSelectedPlate(self, newval):
        self.selected_plate = newval
        self.well_dropdown = create_combo_box(self.appData.getWellNames(self.selected_plate))
        self.patch_path_list = self.appData.getPatchImageFiles(self.selected_plate, self.selected_well, self.selected_measurement)

    def setSelectedWell(self, value):
        self.selected_well = value
        self.patch_path_list = self.appData.getPatchImageFiles(self.selected_plate, self.selected_well, self.selected_measurement)

    def setSelectedMeasurement(self, value):
        self.selected_measurement = value
        self.patch_path_list = self.appData.getPatchImageFiles(self.selected_plate, self.selected_well, self.selected_measurement)

    def setSelectedPatchPath(self, value):
        self.selected_patch_path = value.replace("\\","/")
        if self.selected_patch_path is not None:
            self.page_data["patch_name"] = self.parsePatchName()
            pix = QPixmap(value)
            self.patchImage.setPixmap(pix)
            self.patchImage.adjustSize()
            img_size = self.patchImage.pixmap().size()
            self.patchImage.resize(img_size)
            # self.patchImage.setScaledContents(True)
            # self.patchImage.setImage(value)

    def updated_cellpicture(self):
        print("Inside the update patch picture")
        img_label = QLabel()
        if self.selected_patch_path is not None:
            pixmap = QPixmap(self.selected_patch_path)
            pixmap = pixmap.scaled(50, 50, aspectMode=Qt.KeepAspectRatio)
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignCenter)
        return img_label
    
    def patchImageClicked(self):
        print("Patch image clicked!!!")