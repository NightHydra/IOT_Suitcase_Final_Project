from server_side_handler import ImageHandler
import sys

# Import Pyqt stuff for GUI
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap

from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.__img_handler = ImageHandler()

        # Title of the app
        self.setWindowTitle("MY IOT Suitcase Info Portal")

        self.__sections = self.__generate_sections()

        self.__configure_all_sections(self.__sections)

        # Now place the sections where we need
        col_layout = QHBoxLayout()
        main_layout = QVBoxLayout()

        col_layout.addLayout(self.__sections["ImgShower"])
        col_layout.addLayout(self.__sections["LogShower"])
        

        main_layout.addLayout(self.__sections["TitleShower"])
        main_layout.addLayout(col_layout)

        main_layout.setStretchFactor(col_layout, 2)
        

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def __set_background(self):
        self.setAutoFillBackground(True)

    def __generate_sections(self):
        imglayout = QVBoxLayout()
        loglayout = QVBoxLayout()
        titlelayout = QVBoxLayout()
        

        sections = {"ImgShower" : imglayout, "LogShower": loglayout, "TitleShower" : titlelayout}
        return sections
    
    def __configure_img_shower(self, img_shower):
        refreshButton = QPushButton("Refresh Images")
        refreshButton.clicked.connect(self.__refresh_images)
        # Make a widget to display the image
        self.__image_widget = QLabel(self)
        self.__image_widget.setScaledContents(True)
        
        self.__image_selection_widget = QListWidget()
        # Add the function for when someone selects something in the selection
        #    Widget.  When that happens display the image
        self.__image_selection_widget.currentTextChanged.connect(self.__show_new_img)

        # Add the img showers widget
        img_shower.addWidget(refreshButton,alignment = Qt.AlignHCenter | Qt.AlignTop)
        img_shower.addWidget(self.__image_selection_widget,alignment = Qt.AlignHCenter | Qt.AlignTop)
        img_shower.addWidget(self.__image_widget, alignment = Qt.AlignHCenter | Qt.AlignTop)

    def __configure_log_shower(self, log_shower):
        refreshButton = QPushButton("Refresh Log")
        log_shower.addWidget(refreshButton, alignment = Qt.AlignHCenter | Qt.AlignTop)
    def __configure_title(self, titleshower):
        new_label = QLabel("IOT Suitcase Diagnostics")
        new_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        titleshower.addWidget(new_label)

    def __configure_all_sections(self, sections):
        self.__configure_img_shower(sections["ImgShower"])
        self.__configure_log_shower(sections["LogShower"])
        self.__configure_title(sections["TitleShower"])

    def __refresh_images(self):

        self.__img_handler.request_more_images()
        self.__image_selection_widget.addItems(list(self.__img_handler.get_all_imgnames()))

    def __show_new_img(self, s):

        # Put the image in the widget
        pixmap_to_set_to = QPixmap()
        pixmap_to_set_to.loadFromData(self.__img_handler.get_image_data(s))
        self.__image_widget.setPixmap(pixmap_to_set_to)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()