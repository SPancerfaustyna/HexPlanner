TYPE_MASK   = 0b00001111
ROAD_MASK   = 0b00010000

ZOOM_STEP = 1.15
ZOOM_MIN = -10
ZOOM_MAX = 20

HEX_TYPE_INFO = {
    "label": 0,
    "color": 1
}

CHECKPOINT_STYLE = """
            QCheckBox {
                color: #fff;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
        """

RADIO_BUTTON_STYLE = """
            QRadioButton::indicator {
                width: 12px;
                height: 12px;
                border-radius: 7px;
                border: 1px solid #ddd;
            }

            QRadioButton::indicator:checked {
                background-color: #ddd;
            }
            """
