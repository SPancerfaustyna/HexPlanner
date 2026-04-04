import sys

from PySide6.QtWidgets import QApplication, QComboBox, QHBoxLayout, QMainWindow, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QWidget, QSpinBox, QCheckBox, QPushButton
from PySide6.QtCore import Qt
from HexMap import CustomHexMapScene, HexMapModel, HexMapScene, MapView
import constants
import config

config_data = {
    "small_hex_x_min": config.SMALL_HEX_X_MIN,
    "small_hex_x_max": config.SMALL_HEX_X_MAX,
    "small_hex_x_default": config.SMALL_HEX_X_DEFAULT,
    "small_hex_y_min": config.SMALL_HEX_Y_MIN,
    "small_hex_y_max": config.SMALL_HEX_Y_MAX,
    "small_hex_y_default": config.SMALL_HEX_Y_DEFAULT,
    "large_hex_x_min": config.LARGE_HEX_X_MIN,
    "large_hex_x_max": config.LARGE_HEX_X_MAX,
    "large_hex_x_default": config.LARGE_HEX_X_DEFAULT,
    "large_hex_y_min": config.LARGE_HEX_Y_MIN,
    "large_hex_y_max": config.LARGE_HEX_Y_MAX,
    "large_hex_y_default": config.LARGE_HEX_Y_DEFAULT
}

class Const:
    SmallHex = 0
    LargeHex = 1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HexPlanner")
        self.setGeometry(800, 500, 1000, 600)
        self.config_data = dict(config_data)

        # menuBar = self.menuBar()
        # fileMenu = menuBar.addMenu("File")
        # saveAction = fileMenu.addAction("Save")
        # saveAction.triggered.connect(self.saveMap)
        # loadAction = fileMenu.addAction("Load")
        # loadAction.triggered.connect(self.loadMap)
        # clearMapAction = fileMenu.addAction("Clear Map")
        # clearMapAction.triggered.connect(lambda: self.mapScene.clearMap())

        self.mainContainer = QWidget()
        self.setCentralWidget(self.mainContainer)

        QHBoxLayout(self.mainContainer)
        self.mainContainer.layout().setContentsMargins(0, 0, 0, 0)
        self.mainContainer.layout().setSpacing(0)

        # TODO: Add a container for the map view
        sceneWidth = self.config_data["large_hex_x_max"] - self.config_data["large_hex_x_min"] + 1
        sceneHeight = self.config_data["large_hex_y_max"] - self.config_data["large_hex_y_min"] + 1
        self.mapScene = HexMapScene(HexMapModel(sceneWidth, sceneHeight))
        self.mapScene.setHexHoverCallback(self.setTileInfo)

        self.mapView = MapView()
        self.mapView.setScene(self.mapScene)
        self.mapView.setPaintHexTypeCallback(self.getPaintHexType)
        self.mapView.setPaintRoadCallback(self.getPaintRoad)
        self.mainContainer.layout().addWidget(self.mapView)

        # Side container for controls and coordinates
        self.sideContainer = QWidget()
        self.sideContainer.setStyleSheet("background-color: #333;")
        self.sideContainer.setFixedWidth(200)
        self.mainContainer.layout().addWidget(self.sideContainer)

        QVBoxLayout(self.sideContainer)
        self.sideContainer.layout().setContentsMargins(4, 4, 4, 4)
        self.sideContainer.layout().setSpacing(4)

        # Paint brush
        self.initalizePaintSet()

        # Future: Adding buildings

        self.initializeCustomSet()
        self.sideContainer.layout().addStretch()
        self.initializeTileInfoBox()

    # def saveMap(self):
    #     # Add folder if it doesn't exist
    #     import os
    #     if not os.path.exists("saves"):
    #         os.makedirs("saves")
    #     # Save config
    #     self.mapView.saveMap("saves/hex_map_data", self.config_data)

    # def loadMap(self):
    #     model, newConfigData = HexMapModel.load("saves/hex_map_data")
    #     self.mapScene = HexMapScene(model)
    #     self.mapScene.setHexHoverCallback(self.setTileInfo)
    #     self.mapScene.updateAllHexColors()
    #     if newConfigData is not None:
    #         # Mutate in place so all UI consumers keep the latest values.
    #         self.config_data.clear()
    #         self.config_data.update(newConfigData)

    #     self.mapView.setScene(self.mapScene)
    #     self.updateCoordSpins()

    def initalizePaintSet(self):
        self.paintSetGroup = QGroupBox("Paint Settings")
        QVBoxLayout(self.paintSetGroup)
        self.paintSetGroup.layout().setContentsMargins(4, 4, 4, 4)
        self.paintSetGroup.layout().setSpacing(4)

        self.sideContainer.layout().addWidget(self.paintSetGroup, alignment=Qt.AlignmentFlag.AlignTop)

        setPaintTypeContainer = QWidget()
        QHBoxLayout(setPaintTypeContainer)
        setPaintTypeContainer.layout().setContentsMargins(0, 0, 0, 0)
        setPaintTypeContainer.layout().setSpacing(4)
        self.paintSetGroup.layout().addWidget(setPaintTypeContainer)

        setPaintTypeLabel = QLabel("Set")
        setPaintTypeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        setPaintTypeLabel.setFixedWidth(30)
        setPaintTypeContainer.layout().addWidget(setPaintTypeLabel)

        self.paintSetGroup.setPaintTypeRoadRadio = QRadioButton("Road")
        self.paintSetGroup.setPaintTypeRoadRadio.setStyleSheet(constants.RADIO_BUTTON_STYLE)
        setPaintTypeContainer.layout().addWidget(self.paintSetGroup.setPaintTypeRoadRadio)

        self.paintSetGroup.setPaintTypeHexTypeRadio = QRadioButton("Hex Type")
        self.paintSetGroup.setPaintTypeHexTypeRadio.setStyleSheet(constants.RADIO_BUTTON_STYLE)
        self.paintSetGroup.setPaintTypeHexTypeRadio.setChecked(True)
        setPaintTypeContainer.layout().addWidget(self.paintSetGroup.setPaintTypeHexTypeRadio)

        self.paintSetGroup.setPaintTypeHexTypeRadio.toggled.connect(self.changePaintSet)

        self.paintSetGroup.paintHexTypeCombo = QComboBox()
        for hexType in config.HEX_TYPES:
            self.paintSetGroup.paintHexTypeCombo.addItem(hexType[constants.HEX_TYPE_INFO["label"]])
        self.paintSetGroup.layout().addWidget(self.paintSetGroup.paintHexTypeCombo)

        self.paintSetGroup.roadCheck = QCheckBox("Paint Road")
        self.paintSetGroup.roadCheck.setStyleSheet(constants.CHECKPOINT_STYLE)
        self.paintSetGroup.roadCheck.setHidden(True)
        self.paintSetGroup.layout().addWidget(self.paintSetGroup.roadCheck)

    def changePaintSet(self):
        self.paintSetGroup.paintHexTypeCombo.setHidden(not self.paintSetGroup.setPaintTypeHexTypeRadio.isChecked())
        self.paintSetGroup.roadCheck.setHidden(not self.paintSetGroup.setPaintTypeRoadRadio.isChecked())

        self.mapView.setPaintRoad(self.paintSetGroup.setPaintTypeRoadRadio.isChecked())

    def getPaintHexType(self):
        return self.paintSetGroup.paintHexTypeCombo.currentIndex()
    
    def getPaintRoad(self):
        return self.paintSetGroup.roadCheck.isChecked()

    def initializeCustomSet(self):
        # Set specific type to specific coordinates
        self.specificSetGroup = QGroupBox("Specific Set")
        self.sideContainer.layout().addWidget(self.specificSetGroup, alignment=Qt.AlignmentFlag.AlignTop)
        QVBoxLayout(self.specificSetGroup)
        self.specificSetGroup.layout().setContentsMargins(4, 4, 4, 4)
        self.specificSetGroup.layout().setSpacing(4)

        # checkbox to select if the coordinates are for small or large hex, turns green if large hex is selected, red if small hex is selected
        self.largeHexCheck = QCheckBox("Use Large Hex")
        self.largeHexCheck.setStyleSheet(constants.CHECKPOINT_STYLE)
        self.largeHexCheck.setChecked(True)
        self.largeHexCheck.stateChanged.connect(self.updateCoordSpins)
        self.largeHexCheck.hide()

        self.specificSetGroup.layout().addWidget(self.largeHexCheck)

        # X Coordinate
        xCoordContainer = QWidget()
        QHBoxLayout(xCoordContainer)
        xCoordContainer.layout().setContentsMargins(0, 0, 0, 0)
        xCoordContainer.layout().setSpacing(4)
        self.specificSetGroup.layout().addWidget(xCoordContainer)

        xCoordLabel = QLabel("X:")
        xCoordLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        xCoordLabel.setFixedWidth(10)
        xCoordContainer.layout().addWidget(xCoordLabel)

        self.specificSetGroup.xSpin = QSpinBox()
        xCoordContainer.layout().addWidget(self.specificSetGroup.xSpin)

        # Y Coordinate
        yCoordContainer = QWidget()
        QHBoxLayout(yCoordContainer)
        yCoordContainer.layout().setContentsMargins(0, 0, 0, 0)
        yCoordContainer.layout().setSpacing(4)
        self.specificSetGroup.layout().addWidget(yCoordContainer)

        yCoordLabel = QLabel("Y:")
        yCoordLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        yCoordLabel.setFixedWidth(10)
        yCoordContainer.layout().addWidget(yCoordLabel)

        self.specificSetGroup.ySpin = QSpinBox()
        yCoordContainer.layout().addWidget(self.specificSetGroup.ySpin)

        self.updateCoordSpins()

        setTypeContainer = QWidget()
        QHBoxLayout(setTypeContainer)
        setTypeContainer.layout().setContentsMargins(0, 0, 0, 0)
        setTypeContainer.layout().setSpacing(4)
        self.specificSetGroup.layout().addWidget(setTypeContainer)

        setTypeLabel = QLabel("Set")
        setTypeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        setTypeLabel.setFixedWidth(30)
        setTypeContainer.layout().addWidget(setTypeLabel)

        self.customSetRoadRadio = QRadioButton("Road")
        self.customSetRoadRadio.setStyleSheet(constants.RADIO_BUTTON_STYLE)

        setTypeContainer.layout().addWidget(self.customSetRoadRadio)

        self.customSetHexTypeRadio = QRadioButton("Hex Type")
        self.customSetHexTypeRadio.setStyleSheet(constants.RADIO_BUTTON_STYLE)
        self.customSetHexTypeRadio.setChecked(True)
        setTypeContainer.layout().addWidget(self.customSetHexTypeRadio)

        self.customSetHexTypeRadio.toggled.connect(lambda: self.specificSetGroup.hexTypeCombo.setHidden(not self.customSetHexTypeRadio.isChecked()))

        # Hex type selector
        self.specificSetGroup.hexTypeCombo = QComboBox()
        for hexType in config.HEX_TYPES:
            self.specificSetGroup.hexTypeCombo.addItem(hexType[constants.HEX_TYPE_INFO["label"]])

        self.specificSetGroup.layout().addWidget(self.specificSetGroup.hexTypeCombo)

        # Apply button to set the coordinates to the selected values
        applyButton = QPushButton("Apply")
        applyButton.clicked.connect(self.setCustomSet)
        self.specificSetGroup.layout().addWidget(applyButton)

    def updateCoordSpins(self):
        # Update the range of the spin boxes based on the state of the checkbox
        if self.largeHexCheck.isChecked():
            self.specificSetGroup.xSpin.setRange(self.config_data["large_hex_x_min"], self.config_data["large_hex_x_max"])
            self.specificSetGroup.xSpin.setValue(self.config_data["large_hex_x_default"])

            self.specificSetGroup.ySpin.setRange(self.config_data["large_hex_y_min"], self.config_data["large_hex_y_max"])
            self.specificSetGroup.ySpin.setValue(self.config_data["large_hex_y_default"])
        else:
            self.specificSetGroup.xSpin.setRange(self.config_data["small_hex_x_min"], self.config_data["small_hex_x_max"])
            self.specificSetGroup.xSpin.setValue(self.config_data["small_hex_x_default"])

            self.specificSetGroup.ySpin.setRange(self.config_data["small_hex_y_min"], self.config_data["small_hex_y_max"])
            self.specificSetGroup.ySpin.setValue(self.config_data["small_hex_y_default"])

    def setCustomSet(self):
        x = self.specificSetGroup.xSpin.value() - self.config_data["large_hex_x_min"]
        y = self.specificSetGroup.ySpin.value() - self.config_data["large_hex_y_min"]

        if self.customSetRoadRadio.isChecked():
            self.mapScene.model.setRoad(x, y, True)
        elif self.customSetHexTypeRadio.isChecked():
            hexType = self.specificSetGroup.hexTypeCombo.currentIndex()
            self.mapScene.setHexType(x, y, hexType)

        # Convert to large hex coordinates if the checkbox is not checked
        # if not self.largeHexCheck.isChecked():
        #     x = x - config.SMALL_HEX_X_MIN + config.LARGE_HEX_X_MIN
        #     y = y - config.SMALL_HEX_Y_MIN + config.LARGE_HEX_Y_MIN

    def initializeTileInfoBox(self):
        tileInfoGroup = QGroupBox("Tile Info")
        QVBoxLayout(tileInfoGroup)
        tileInfoGroup.layout().setContentsMargins(4, 4, 4, 4)
        tileInfoGroup.layout().setSpacing(4)

        self.sideContainer.layout().addWidget(tileInfoGroup, alignment=Qt.AlignmentFlag.AlignBottom)

        self.smallHexCoordLabel = QLabel("Small Hex: (None, None)")
        self.smallHexCoordLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tileInfoGroup.layout().addWidget(self.smallHexCoordLabel)

        self.largeHexCoordLabel = QLabel("Large Hex: (None, None)")
        self.largeHexCoordLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tileInfoGroup.layout().addWidget(self.largeHexCoordLabel)

        self.tileTypeLabel = QLabel("Tile Type: None")
        self.tileTypeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tileInfoGroup.layout().addWidget(self.tileTypeLabel)

        self.isRoadLabel = QLabel("Road: None")
        self.isRoadLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tileInfoGroup.layout().addWidget(self.isRoadLabel)

    def setTileInfo(self, x, y):
        # self.smallHexCoordLabel.setText(f"Small Hex: ({x + config.SMALL_HEX_X_MIN}, {y + config.SMALL_HEX_Y_MIN})")
        self.largeHexCoordLabel.setText(f"Large Hex: ({x + self.config_data['large_hex_x_min']}, {y + self.config_data['large_hex_y_min']})")
        self.tileTypeLabel.setText(f"Tile Type: {self.mapScene.model.getHexType(x, y)}")
        self.isRoadLabel.setText(f"Road: {'Yes' if self.mapScene.model.hasRoad(x, y) else 'No'}")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
