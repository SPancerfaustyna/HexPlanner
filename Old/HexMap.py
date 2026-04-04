import math

from PySide6 import QtGui
import numpy as np
from PySide6.QtWidgets import QApplication, QGraphicsItem, QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPen, QPolygonF
from PySide6.QtCore import QPointF, Qt, QRectF
import constants
import config

class TileBits:
    @staticmethod
    def get_type(value: int) -> int:
        return value & constants.TYPE_MASK

    @staticmethod
    def set_type(value: int, tile_type: int) -> int:
        clear_mask = 0xFF ^ constants.TYPE_MASK
        return (int(value) & clear_mask) | (int(tile_type) & constants.TYPE_MASK)

    @staticmethod
    def has_road(value: int) -> bool:
        return bool(value & constants.ROAD_MASK)

    @staticmethod
    def set_road(value: int, enabled: bool) -> int:
        if enabled:
            return int(value) | constants.ROAD_MASK
        clear_mask = 0xFF ^ constants.ROAD_MASK
        return int(value) & clear_mask

class HexMapModel:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.meta = np.zeros((height, width), dtype=np.uint8)
        self.heights = np.zeros((height, width), dtype=np.uint8)

    def getHexType(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            type_value = TileBits.get_type(self.meta[y, x])
            return config.HEX_TYPES[type_value][constants.HEX_TYPE_INFO["label"]] if type_value < len(config.HEX_TYPES) else "Unknown"
        return None
    
    def setHexType(self, x: int, y: int, tile_type: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.meta[y, x] = TileBits.set_type(self.meta[y, x], tile_type)

    def hasRoad(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return TileBits.has_road(self.meta[y, x])
        return False
    
    def setRoad(self, x: int, y: int, enabled: bool):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.meta[y, x] = TileBits.set_road(self.meta[y, x], enabled)

    def save(self, path: str, config_data) -> None:
        # print(extra)

        np.savez_compressed(
            path,
            version=1,
            width=self.width,
            height=self.height,
            meta=self.meta,
            heights=self.heights,
            small_hex_x_min=config_data["small_hex_x_min"],
            small_hex_x_max=config_data["small_hex_x_max"],
            small_hex_x_default=config_data["small_hex_x_default"],
            small_hex_y_min=config_data["small_hex_y_min"],
            small_hex_y_max=config_data["small_hex_y_max"],
            small_hex_y_default=config_data["small_hex_y_default"],
            large_hex_x_min=config_data["large_hex_x_min"],
            large_hex_x_max=config_data["large_hex_x_max"],
            large_hex_x_default=config_data["large_hex_x_default"],
            large_hex_y_min=config_data["large_hex_y_min"],
            large_hex_y_max=config_data["large_hex_y_max"],
            large_hex_y_default=config_data["large_hex_y_default"],
        )

    @classmethod
    def load(cls, path: str) -> "HexMapModel":
        data = np.load(path + ".npz")

        version = int(data["version"])
        if version != 1:
            raise ValueError(f"Unsupported file version: {version}")

        width = int(data["width"])
        height = int(data["height"])

        model = cls(width, height)
        model.meta = data["meta"]
        model.heights = data["heights"]#
        
        config_data = {
            "small_hex_x_min": int(data["small_hex_x_min"]),
            "small_hex_x_max": int(data["small_hex_x_max"]),
            "small_hex_x_default": int(data["small_hex_x_default"]),
            "small_hex_y_min": int(data["small_hex_y_min"]),
            "small_hex_y_max": int(data["small_hex_y_max"]),
            "small_hex_y_default": int(data["small_hex_y_default"]),
            "large_hex_x_min": int(data["large_hex_x_min"]),
            "large_hex_x_max": int(data["large_hex_x_max"]),
            "large_hex_x_default": int(data["large_hex_x_default"]),
            "large_hex_y_min": int(data["large_hex_y_min"]),
            "large_hex_y_max": int(data["large_hex_y_max"]),
            "large_hex_y_default": int(data["large_hex_y_default"])
        }
        return (model, config_data)


class HexMapItem(QGraphicsPolygonItem):
    RADIUS = config.HEX_RADIUS
    HALF = RADIUS / 2
    WIDE = math.sqrt(3) / 2 * RADIUS

    POINT_OFFSET = [
        (0, -RADIUS),
        (WIDE, -HALF),
        (WIDE, HALF),
        (0, RADIUS),
        (-WIDE, HALF),
        (-WIDE, -HALF)
    ]

    def __init__(self, grid_x: int, grid_y: int, cx: int, cy: int):
        points = [QPointF(cx + dx, cy + dy) for dx, dy in self.POINT_OFFSET]
        super().__init__(QPolygonF(points))

        self.world_x = cx
        self.world_y = cy
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        scene = self.scene()
        if scene is not None and hasattr(scene, "on_hex_hovered"):
            scene.on_hex_hovered(self.grid_x, self.grid_y)
        super().hoverEnterEvent(event)


class HexMapScene(QGraphicsScene):

    HSTEP = math.sqrt(3) * config.HEX_RADIUS
    VSTEP = 1.5 * config.HEX_RADIUS

    def __init__(self, model: HexMapModel):
        super().__init__()
        self.model = model
        self.hoverCoords = (-1, -1)

        whitePen = QPen(Qt.GlobalColor.white)
        whitePen.setWidth(1)

        for x in range(0, model.width, 1):
            for y in range(0, model.height, 1):
                cx = x * self.HSTEP + (y % 2) * self.HSTEP / 2
                cy = y * self.VSTEP

                hexItem = HexMapItem(x, y, cx, cy)
                hexItem.setPen(whitePen)
                hexItem.setBrush(QtGui.QColor(config.HEX_TYPES[0][constants.HEX_TYPE_INFO["color"]]))
                self.addItem(hexItem)

    def setHexHoverCallback(self, callback):
        self.onHexHoverCallback = callback

    def on_hex_hovered(self, x: int, y: int):
        self.hoverCoords = (x, y)
        if hasattr(self, "onHexHoverCallback") and self.onHexHoverCallback is not None:
            self.onHexHoverCallback(x, y)

    def setHexType(self, x: int, y: int, tile_type: int):
        if 0 <= x < self.model.width and 0 <= y < self.model.height:
            self.model.setHexType(x, y, tile_type)
            self.updateHexColor(x, y)

    def setHexRoad(self, x: int, y: int, has_road: bool):
        if 0 <= x < self.model.width and 0 <= y < self.model.height:
            self.model.setRoad(x, y, has_road)


    def updateHexColor(self, x: int, y: int):
        tile_type = TileBits.get_type(self.model.meta[y, x])
        color = config.HEX_TYPES[tile_type][constants.HEX_TYPE_INFO["color"]] if tile_type < len(config.HEX_TYPES) else "#000000"

        for item in self.items():
            if isinstance(item, HexMapItem) and item.grid_x == x and item.grid_y == y:
                item.setBrush(QtGui.QColor(color))
                break
    
    def updateAllHexColors(self):
        for x in range(self.model.width):
            for y in range(self.model.height):
                self.updateHexColor(x, y)

    # draw road as a line to surrounding hexes with roads or circle if no surrounding roads
    def updateHexRoad(self, x: int, y: int):
        has_road = self.model.hasRoad(x, y)
        for item in self.items():
            if isinstance(item, HexMapItem) and item.grid_x == x and item.grid_y == y:
                # print positions of neighboring hexes
                if has_road:
                    rect = QRectF(item.world_x - 5, item.world_y - 5, 10, 10)
                    self.addEllipse(rect, QPen(Qt.GlobalColor.red), QtGui.QBrush(Qt.GlobalColor.red))
                break


class CustomHexMapScene(QGraphicsScene):
    def __init__(self, model: HexMapModel):
        super().__init__()
        self.model = model

        self._terrain_brushes = {
            0: QtGui.QBrush("#228B22"),  # Grass
            1: QtGui.QBrush("#8B4513"),  # Dirt
            2: QtGui.QBrush("#1E90FF"),  # Water
        }

        self._grid_pen = QPen(Qt.GlobalColor.white)

        hexItem = self.hex_polygon(QPointF(50, 50))
        hexItem = QGraphicsPolygonItem(hexItem)
        hexItem.setPen(self._grid_pen)
        # hexItem.setBrush(QtGui.QColor(config.HEX_TYPES[0][constants.HEX_TYPE_INFO["color"]]))
        self.addItem(hexItem)

    def hex_polygon(self, center: QPointF) -> QPolygonF:
        pts = []
        # pointy-top hex
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            x = center.x() + 100 * math.cos(angle_rad)
            y = center.y() + 100 * math.sin(angle_rad)
            pts.append(QPointF(x, y))
        return QPolygonF(pts)

    def drawBackground(self, painter, rect):
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        painter.setPen(self._grid_pen)

        painter.setBrush(self._terrain_brushes[0])
        painter.drawPolygon(self.hex_polygon(QPointF(100, 100)))
        painter.drawPolygon(self.hex_polygon(QPointF(200, 200)))
        painter.drawPolygon(self.hex_polygon(QPointF(300, 300)))


        return super().drawBackground(painter, rect)


class MapView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.zoom = 0
        self.zoomStep = constants.ZOOM_STEP
        self.zoomMin = constants.ZOOM_MIN
        self.zoomMax = constants.ZOOM_MAX
        self.isPainting = False
        self.lastPainted = None
        self.isRoadPainting = False

        self.setStyleSheet("background-color: #222;")
        self.setStyleSheet("border: none;")

        self.setRenderHints(self.renderHints())
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def saveMap(self, path: str, configData) -> None:
        if self.scene() is not None and hasattr(self.scene(), "model"):
            self.scene().model.save(path, configData)

    # Map zooming with mouse wheel
    def wheelEvent(self, event):
        angle = event.angleDelta().y()

        if angle == 0:
            return
        
        if angle > 0:
            if self.zoom >= self.zoomMax:
                return
            factor = self.zoomStep
            self.zoom += 1
        else:
            if self.zoom <= self.zoomMin:
                return
            factor = 1 / self.zoomStep
            self.zoom -= 1

        self.scale(factor, factor)

    def setPaintHexTypeCallback(self, callback):
        self.getPaintHexType = callback

    def setPaintRoadCallback(self, callback):
        self.getPaintRoad = callback

    def paintAt(self, viewportPos):
        scene = self.scene()
        if scene is None or not hasattr(self, "getPaintHexType"):
            return

        scenePos = self.mapToScene(viewportPos)
        for item in scene.items(scenePos):
            if isinstance(item, HexMapItem):
                coords = (item.grid_x, item.grid_y)
                if coords == self.lastPainted:
                    return
                if self.isRoadPainting:
                    scene.setHexRoad(item.grid_x, item.grid_y, self.getPaintRoad())
                else:
                    scene.setHexType(item.grid_x, item.grid_y, self.getPaintHexType())

                self.lastPainted = coords
                self.scene().on_hex_hovered(item.grid_x, item.grid_y)
                self.scene().updateHexRoad(item.grid_x, item.grid_y)
                return

    def setPaintRoad(self, enabled: bool):
        self.isRoadPainting = enabled

    def mousePressEvent(self, event):
        # Map dragging when ctrl is held down
        if event.button() == Qt.MouseButton.LeftButton and QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)
            self.isPainting = False
        # Map painting when mouse is clicked without ctrl
        elif event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.viewport().setCursor(Qt.CursorShape.CrossCursor)
            self.isPainting = True
            self.lastPainted = None
            self.paintAt(event.position().toPoint())

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.isPainting:
            self.paintAt(event.position().toPoint())

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            self.isPainting = False
            self.lastPainted = None
        
        super().mouseReleaseEvent(event)
