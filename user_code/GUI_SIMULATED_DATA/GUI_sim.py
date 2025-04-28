from server_side_handler import ImageHandler, SensorHandler
import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Image and Sensor handlers
        self.__img_handler = ImageHandler()
        self.sensor_handler = SensorHandler()

        # Login to server
        self.__img_handler.login_to_server("alice", "password123")

        # Window title
        self.setWindowTitle("MY IOT Suitcase Info Portal")

        # Generate and configure sections
        self.__sections = self.__generate_sections()
        self.__configure_all_sections(self.__sections)

        # Layout assembly with 2:1 stretch for image:log
        layout = QHBoxLayout()
        layout.addLayout(self.__sections["ImgShower"], 2)
        layout.addLayout(self.__sections["LogShower"], 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.__sections["TitleShower"])
        main_layout.addLayout(layout)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def __generate_sections(self):
        return {
            "ImgShower": QVBoxLayout(),
            "LogShower": QVBoxLayout(),
            "TitleShower": QVBoxLayout()
        }

    def __configure_img_shower(self, img_shower):
        # Unchanged from original
        refresh_btn = QPushButton("Refresh Images")
        refresh_btn.clicked.connect(self.__refresh_images)
        self.__image_selection_widget = QListWidget()
        self.__image_selection_widget.currentTextChanged.connect(self.__show_new_img)
        self.__image_widget = QLabel()
        self.__image_widget.setAlignment(Qt.AlignCenter)

        img_shower.addWidget(refresh_btn, alignment=Qt.AlignHCenter | Qt.AlignTop)
        img_shower.addWidget(self.__image_selection_widget, alignment=Qt.AlignHCenter | Qt.AlignTop)
        img_shower.addWidget(self.__image_widget, alignment=Qt.AlignHCenter | Qt.AlignTop)

    def __configure_log_shower(self, log_shower):
        # Add title for log panel
        title_lbl = QLabel("Event Log")
        title_lbl.setAlignment(Qt.AlignCenter)
        log_shower.addWidget(title_lbl)

        refresh_btn = QPushButton("Refresh Log")
        refresh_btn.clicked.connect(self.__refresh_log)
        log_shower.addWidget(refresh_btn, alignment=Qt.AlignHCenter | Qt.AlignTop)

        self.__log_list = QListWidget()
        # Let log list expand vertically, narrow horizontally by stretch
        self.__log_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        log_shower.addWidget(self.__log_list)

    def __configure_title(self, titleshower):
        lbl = QLabel("IOT Suitcase Diagnostics")
        lbl.setAlignment(Qt.AlignCenter)
        titleshower.addWidget(lbl)

    def __configure_all_sections(self, sections):
        self.__configure_title(sections["TitleShower"])
        self.__configure_img_shower(sections["ImgShower"])
        self.__configure_log_shower(sections["LogShower"])

    def __refresh_images(self):
        self.__img_handler.request_more_images()
        self.__image_selection_widget.clear()
        self.__image_selection_widget.addItems(list(self.__img_handler.get_all_imgnames()))

    def __show_new_img(self, fname):
        pix = QPixmap()
        pix.loadFromData(self.__img_handler.get_image_data(fname))
        self.__image_widget.setPixmap(pix.scaled(300, 300, Qt.KeepAspectRatio))

    def __refresh_log(self):
        events = self.sensor_handler.get_recent_events()
        for e in events:
            if e["type"] == "SWITCH":
                text = f"{e['timestamp']}: Switch {e['state']}"
            elif e["type"] == "PUSH":
                text = f"{e['timestamp']}: Push detected (magnitude: {e['magnitude']})"
            elif e["type"] == "GPS":
                text = f"{e['timestamp']}: GPS coords: {e['lat']:.6f}, {e['lon']:.6f}"
            else:
                text = str(e)
            self.__log_list.addItem(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
