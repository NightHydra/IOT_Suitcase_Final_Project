# GUI.py
from server_side_handler import DataHandler
import sys

# Import Pyqt stuff for GUI
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QSizePolicy, QLineEdit, QStackedWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap

from PyQt5.QtCore import Qt

class MainApplicationWindow(QMainWindow):

    def __init__(self, server_handler : DataHandler):
        super().__init__()

        self.__img_handler = server_handler

        self.setWindowTitle("MY IOT Suitcase Info Portal")
        self.build_ui()

    def build_ui(self):
        # Title
        title_lbl = QLabel("IOT Suitcase Diagnostic Portal")
        title_lbl.setAlignment(Qt.AlignCenter)

        self.__set_font_size(title_lbl, 24)

        # Image panel
        refresh_img_btn = QPushButton("Refresh Images")
        refresh_img_btn.clicked.connect(self.refresh_images)

        self.image_list   = QListWidget()
        self.image_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.image_list.setMinimumWidth(350)
        self.image_list.currentTextChanged.connect(self.show_image)
        self.image_label  = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        img_layout = QVBoxLayout()
        img_layout.addWidget(refresh_img_btn)
        img_layout.addWidget(self.image_list, 2)
        img_layout.addWidget(self.image_label,  alignment=Qt.AlignHCenter|Qt.AlignCenter)

        # Log panel
        #log_title      = QLabel("Event Log")
        #log_title.setAlignment(Qt.AlignCenter)
        refresh_log_btn = QPushButton("Refresh Log")
        refresh_log_btn.clicked.connect(self.__update_event_data)
        #refresh_log_btn.clicked.connect(self.refresh_log)
        self.log_list   = QListWidget()
        self.log_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        log_layout = QVBoxLayout()
        #log_layout.addWidget(log_title)
        log_layout.addWidget(refresh_log_btn)
        log_layout.addWidget(self.log_list)

        # Combine image and log panels (1:1 width)
        main_h = QHBoxLayout()
        main_h.addLayout(img_layout, 1)
        main_h.addLayout(log_layout, 1)

        # Final layout
        main_v = QVBoxLayout()
        main_v.addWidget(title_lbl)
        main_v.addLayout(main_h)

        container = QWidget()
        container.setLayout(main_v)
        self.setCentralWidget(container)

    def refresh_images(self):
        self.__img_handler.request_more_images()
        self.image_list.addItems(self.__img_handler.get_new_imagenames())

    def show_image(self, name: str):
        pix = QPixmap()
        pix.loadFromData(self.__img_handler.get_image_data(name))
        self.image_label.setPixmap(pix.scaled(750,750,Qt.KeepAspectRatio))
    

    def __configure_log_shower(self, log_shower):
        refreshButton = QPushButton("Refresh Log")
        log_shower.addWidget(refreshButton, alignment = Qt.AlignHCenter | Qt.AlignTop)
    def __configure_title(self, titleshower):
        new_label = QLabel("IOT Suitcase Diagnostics")
        new_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        titleshower.addWidget(new_label)

    def __set_font_size(self, label, size):
        font = self.font()
        font.setPointSize(size)
        label.setFont(font)
    
    def __update_event_data(self):
        events = self.__img_handler.get_event_data()
        
        for e in events:
            print (e)
            if e['type'] == 'SWITCH':
                text = f"{e['timestamp']}: Switch {e['state']}"
            elif e['type'] == 'PUSH':
                text = f"{e['timestamp']}: Push detected (magnitude: {e['magnitude']})"
            elif e['type'] == 'GPS':
                text = f"{e['timestamp']}: GPS coords: {e['lat']:.4f}, {e['lon']:.4f}"
            else:
                text = str(e)
            self.log_list.insertItem(0, text)

    def __configure_all_sections(self, sections):
        self.__configure_img_shower(sections["ImgShower"])
        self.__configure_log_shower(sections["LogShower"])
        self.__configure_title(sections["TitleShower"])

    def __refresh_images(self):

        self.__img_handler.request_more_images()

        for imgname in reversed(self.__img_handler.get_new_imagenames()):
            self.__image_selection_widget.insertItem(0, imgname)

    def __show_new_img(self, s):

        # Put the image in the widget
        pixmap_to_set_to = QPixmap()
        pixmap_to_set_to.loadFromData(self.__img_handler.get_image_data(s))
        # self.__image_widget.setPixmap(pixmap_to_set_to.scaled(300, 300, Qt.KeepAspectRatio))   
        self.__image_widget.setPixmap(pixmap_to_set_to)    

class LoginScreenMainWindow(QMainWindow):

    def __init__(self, stacked_widg):

        super().__init__()

        self.__the_stacked_widget = stacked_widg

        screen_rows = self.__generate_screen_layout_sections()

        self.__configure_title_row(screen_rows["title"])
        self.__configure_username_and_password_rows(screen_rows['uname'], screen_rows['pwd'])
        self.__configure_login_press_box(screen_rows['login'])

        main_layout = QVBoxLayout()

        main_layout.addLayout(screen_rows['title'], stretch =0)
        main_layout.addLayout(screen_rows['uname'], stretch = 0)
        main_layout.addLayout(screen_rows['pwd'], stretch = 0)
        main_layout.addLayout(screen_rows['login'], stretch = 2)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        
    def __generate_screen_layout_sections(self):

        title_box = QHBoxLayout()
        username_box = QHBoxLayout()
        password_box = QHBoxLayout()
        login_box = QHBoxLayout()

        return {"title" : title_box, "uname" : username_box, "pwd" : password_box, "login" : login_box}
    
    def __configure_title_row(self, layout_box : QHBoxLayout):

        title_lab = QLabel("IOT Suitcase Login Page")
        self.__set_font_size(title_lab, 16)
        layout_box.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout_box.addWidget(title_lab)

    def __configure_username_and_password_rows(self, uname_hbox : QHBoxLayout, pwd_hbox : QHBoxLayout):

        uname_lab = QLabel("Enter Username: ")
        self.__uname_enter_box = QLineEdit()
        self.__set_font_size(uname_lab, 16)
        self.__set_font_size(self.__uname_enter_box, 16)

        pwd_lab = QLabel("Enter Password: ")
        self.__pwd_enter_box = QLineEdit()
        self.__pwd_enter_box.setEchoMode(QLineEdit.Password)
        self.__set_font_size(pwd_lab, 16)
        self.__set_font_size(self.__pwd_enter_box, 16)

        uname_hbox.addWidget(uname_lab)
        uname_hbox.addWidget(self.__uname_enter_box)

        pwd_hbox.addWidget(pwd_lab)
        pwd_hbox.addWidget(self.__pwd_enter_box)

    def __configure_login_press_box(self, login_box : QHBoxLayout):

        loginButton = QPushButton("Login")
        loginButton.clicked.connect(self.__go_past_login_screen)

        login_box.addWidget(loginButton, Qt.AlignCenter)

    def __go_past_login_screen(self):

        uname = self.__uname_enter_box.text()
        pwd = self.__pwd_enter_box.text()

        server_hand = DataHandler()

        success = server_hand.login_to_server(uname, pwd)

        if not success:
            return

        new_window = MainApplicationWindow(server_hand)

        self.__the_stacked_widget.addWidget(new_window)
        
        self.__the_stacked_widget.setCurrentWidget(new_window)
    
    def __set_font_size(self, label, size):
        font = self.font()
        font.setPointSize(size)
        label.setFont(font)
        

app = QApplication(sys.argv)

stacked_widget = QStackedWidget()

login_page = LoginScreenMainWindow(stacked_widget)

stacked_widget.addWidget(login_page)

stacked_widget.setCurrentWidget(login_page)

stacked_widget.show()

app.exec()
