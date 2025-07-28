from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QFrame, QTextEdit
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from pythonosc.udp_client import SimpleUDPClient
import serial
import serial.tools.list_ports
import sys
from pathlib import Path
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

# Handle PyInstaller and normal dev environment
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)  # PyInstaller runtime path
else:
    BASE_DIR = Path(__file__).resolve().parent


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port, baud, command_1, command_2, column_1, column_2):
        super().__init__()
        self.port = port
        self.baud = baud
        self.command_1 = command_1
        self.command_2 = command_2
        self.column_1 = column_1
        self.column_2 = column_2
        self.running = True
        self.client = SimpleUDPClient("127.0.0.1", 7000)

    def run(self):
        try:
            ser = serial.Serial(self.port, int(self.baud), timeout=1)
            ser.reset_input_buffer()
            while self.running:
                if ser.in_waiting > 0:
                    raw = ser.readline()
                    try:
                        data = raw.decode('utf-8').strip()
                    except UnicodeDecodeError:
                        data = raw.decode('latin1').strip()

                    self.data_received.emit(data)

                    if data == self.command_1:
                        self.client.send_message(f"/composition/columns/{self.column_1}/connect", 1)
                    elif data == self.command_2:
                        self.client.send_message(f"/composition/columns/{self.column_2}/connect", 1)
            ser.close()
        except Exception as e:
            self.data_received.emit(f"Serial Error: {str(e)}")

    def stop(self):
        self.running = False
        self.wait()


class SerialUI(QWidget):
    def __init__(self):
        super().__init__()

        self.base_width = 1920
        self.base_height = 1080
        self.resize(self.base_width, self.base_height)

       

        self.setWindowTitle("MME Serial Listener")
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowIcon(QIcon(str(BASE_DIR / "Asset 1.ico")))
        

        self.serial_thread = None

        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(str(BASE_DIR / "Asset 3.png")))
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(0, 0, 1920, 1080)
        self.bg_label.lower()  # Send to back


        self.frame = QFrame(self)
        self.frame.setGeometry(420, 240, 1072, 649)

        self.bg_label_inside_frame = QLabel(self.frame)
        pixmap = QPixmap(str(BASE_DIR / "Asset 11.png"))
        self.bg_label_inside_frame.setPixmap(pixmap)
        self.bg_label_inside_frame.setScaledContents(True)
        self.bg_label_inside_frame.setGeometry(0, 0, self.frame.width(), self.frame.height())


        # ---------- UI Elements ----------
        self.com_port_img = QLabel(self)
        self.com_port_img.setPixmap(QPixmap(str(BASE_DIR / "Asset 13.png")))
        self.com_port_img.setGeometry(560, 340, 338, 77)
        self.com_port_img.setScaledContents(True)

        self.port_dropdown = QComboBox(self)
        self.port_dropdown.setGeometry(580, 380, 300, 30)  # Positioned inside the input box
        self.port_dropdown.addItems(list_serial_ports())
        self.port_dropdown.setStyleSheet("""
    QComboBox {
                 background-color: rgba(255, 255, 255, 0);  /* transparent */
                 background-image: url(str(BASE_DIR / "Asset 12.png"));
                 background-repeat: no-repeat;
                 background-position: center;
                border: none;
    }
    QComboBox QAbstractItemView {
        background-color: white;  /* dropdown list background */
        color: black;
    }
""")
        
        self.baud_img = QLabel(self)
        self.baud_img.setPixmap(QPixmap(str(BASE_DIR / "Asset 7.png")))
        self.baud_img.setGeometry(1000, 340, 338, 77)
        self.baud_img.setScaledContents(True)
        
        
        self.baud_edit = QLineEdit(self)
        self.baud_edit.setGeometry(1020, 380, 300, 30)
        self.baud_edit.setStyleSheet("""
    QLineEdit {
                 background-color: rgba(255, 255, 255, 0);  /* transparent */
                 background-image: url(str(BASE_DIR / "Asset 12.png"));
                 background-repeat: no-repeat;
                 background-position: center;
                border: none;
    }
    QComboBox QAbstractItemView {
        background-color: white;  /* dropdown list background */
        color: black;
    }
""")
        self.cmd1_img = QLabel(self)
        self.cmd1_img.setPixmap(QPixmap(str(BASE_DIR / "Asset 8.png")))
        self.cmd1_img.setGeometry(560, 450, 338, 77)
        self.cmd1_img.setScaledContents(True)


        self.cmd1_edit = QLineEdit(self)
        self.cmd1_edit.setGeometry(580, 490, 300, 30)
        self.cmd1_edit.setStyleSheet("""
    QLineEdit {
                 background-color: rgba(255, 255, 255, 0);  /* transparent */
                 background-image: url(str(BASE_DIR / "Asset 12.png"));
                 background-repeat: no-repeat;
                 background-position: center;
                border: none;
    }
    QComboBox QAbstractItemView {
        background-color: white;  /* dropdown list background */
        color: black;
    }
""")
        
        
        self.cmd2_img = QLabel(self)
        self.cmd2_img.setPixmap(QPixmap(str(BASE_DIR / "Asset 14.png")))
        self.cmd2_img.setGeometry(1000, 450, 338, 77)
        self.cmd2_img.setScaledContents(True)


        self.cmd2_edit = QLineEdit(self)
        self.cmd2_edit.setGeometry(1020, 490, 300, 30)
        self.cmd2_edit.setStyleSheet("""
    QLineEdit {
                 background-color: rgba(255, 255, 255, 0);  /* transparent */
                 background-image: url(str(BASE_DIR / "Asset 12.png"));
                 background-repeat: no-repeat;
                 background-position: center;
                 border: none;
    }
    QComboBox QAbstractItemView {
        background-color: white;  /* dropdown list background */
        color: black;
    }
""")
        self.col1_img = QLabel(self)
        self.col1_img.setPixmap(QPixmap(str(BASE_DIR / "Asset 9.png")))
        self.col1_img.setGeometry(560, 560, 338, 77)
        self.col1_img.setScaledContents(True)

        self.col1_dropdown = QComboBox(self)
        self.col1_dropdown.setGeometry(580, 600, 300, 30)
        self.col1_dropdown.addItems([str(i) for i in range(1, 11)])
        self.col1_dropdown.setStyleSheet("""
    QComboBox {
                 background-color: rgba(255, 255, 255, 0);  /* transparent */
                 background-image: url(str(BASE_DIR / "Asset 12.png"));
                 background-repeat: no-repeat;
                 background-position: center;
                 border: none;
    }
    QComboBox QAbstractItemView {
        background-color: white;  /* dropdown list background */
        color: black;
    }
""")
        self.col2_img = QLabel(self)
        self.col2_img.setPixmap(QPixmap(str(BASE_DIR / "Asset 10.png")))
        self.col2_img.setGeometry(1000, 560, 338, 77)
        self.col2_img.setScaledContents(True)
        
        self.col2_dropdown = QComboBox(self)
        self.col2_dropdown.setGeometry(1020, 600, 300, 30)
        self.col2_dropdown.addItems([str(i) for i in range(1, 11)])
        self.col2_dropdown.setStyleSheet("""
    QComboBox {
                 background-color: rgba(255, 255, 255, 0);  /* transparent */
                 background-image: url(str(BASE_DIR / "Asset 12.png"));
                 background-repeat: no-repeat;
                 background-position: center;
                 border: none;
    }
    QComboBox QAbstractItemView {
        background-color: white;  /* dropdown list background */
        color: black;
    }
""")

        self.start_button = QPushButton( self)
        self.start_button.setGeometry(650, 700, 252, 56)
        icon_path = str(BASE_DIR / "Asset 4.png")  # use str if you're using pathlib
        self.start_button.setIcon(QIcon(icon_path))
        self.start_button.setIconSize(QSize(252, 56))
        self.start_button.setStyleSheet("""
    QPushButton {
        border: none;
        background-color: transparent;
    }
""")
        self.start_button.clicked.connect(self.start_listening)

        self.stop_button = QPushButton( self)
        self.stop_button.setGeometry(950, 700, 252, 56)
        icon_path = str(BASE_DIR / "Asset 5.png")  # use str if you're using pathlib
        self.stop_button.setIcon(QIcon(icon_path))
        self.stop_button.setIconSize(QSize(252, 56))
        self.stop_button.setStyleSheet("""
    QPushButton {
        border: none;
        background-color: transparent;
    }
""")
        self.stop_button.clicked.connect(self.stop_listening)

        self.log_box = QTextEdit(self)
        self.log_box.setGeometry(460, 900, 1000, 150)
        self.log_box.setReadOnly(True)
        self.log_box.hide()  # Hidden initially


        # At the end of __init__:
        self.widgets_geometry = {
    self.bg_label: (0, 0, 1920, 1080),
    self.frame: (420, 240, 1072, 649),
    self.com_port_img: (560, 340, 338, 77),
    self.port_dropdown: (580, 380, 300, 30),
    self.baud_img: (1000, 340, 338, 77),
    self.baud_edit: (1020, 380, 300, 30),
    self.cmd1_img: (560, 450, 338, 77),
    self.cmd1_edit: (580, 490, 300, 30),
    self.cmd2_img: (1000, 450, 338, 77),
    self.cmd2_edit: (1020, 490, 300, 30),
    self.col1_img: (560, 560, 338, 77),
    self.col1_dropdown: (580, 600, 300, 30),
    self.col2_img: (1000, 560, 338, 77),
    self.col2_dropdown: (1020, 600, 300, 30),
    self.start_button: (650, 700, 252, 56),
    self.stop_button: (950, 700, 252, 56),
    self.log_box: (460, 900, 1000, 150),
}


    def log(self, message):
        self.log_box.append(message)
        self.log_box.show()

    def resizeEvent(self, event):
       w_scale = self.width() / self.base_width
       h_scale = self.height() / self.base_height

       for widget, (x, y, w, h) in self.widgets_geometry.items():
          new_x = int(x * w_scale)
          new_y = int(y * h_scale)
          new_w = int(w * w_scale)
          new_h = int(h * h_scale)
          widget.setGeometry(new_x, new_y, new_w, new_h)

    # Resize background image to match new window size
       if hasattr(self, 'bg_label'):
        scaled_pixmap = QPixmap(str(BASE_DIR / "Asset 3.png")).scaled(
            self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        self.bg_label.setPixmap(scaled_pixmap)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())

    # Resize bg inside frame
       if hasattr(self, 'bg_label_inside_frame'):
        self.bg_label_inside_frame.setGeometry(0, 0, self.frame.width(), self.frame.height())

       super().resizeEvent(event)




    def start_listening(self):
        port = self.port_dropdown.currentText()
        baud = self.baud_edit.text()
        cmd1 = self.cmd1_edit.text()
        cmd2 = self.cmd2_edit.text()
        col1 = self.col1_dropdown.currentText()
        col2 = self.col2_dropdown.currentText()

        if not port or not baud:
            self.log("Please select port and enter baud rate.")
            return

        self.serial_thread = SerialThread(port, baud, cmd1, cmd2, col1, col2)
        self.serial_thread.data_received.connect(self.log)
        self.serial_thread.start()
        self.log_box.show()
        self.log(f"Listening on {port} at {baud}...")

    def stop_listening(self):
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread = None
            self.log("Serial listener stopped.")
            self.log_box.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialUI()
    window.show()
    sys.exit(app.exec())

    
