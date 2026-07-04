import socket
import struct
import sys
import time

from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot

from fields import FIELDS 


UDP_IP = "127.0.0.1"
UDP_PORT = 8999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.25)

last_draw = 0
draw_rate = 20  # terminal refreshes per second


class TelemetryWorker(QObject):
    telemetry_ready = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.running = True

    @pyqtSlot()
    def run(self):
        global last_draw

        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
            except socket.timeout:
                continue
            except OSError:
                break

            if len(data) not in (323, 324):
                continue

            try:
                t = parse_forza_packet(data)
            except ValueError:
                continue

            now = time.time()
            if now - last_draw < 1 / draw_rate:
                continue

            last_draw = now

            self.telemetry_ready.emit(t)

    def stop(self):
        self.running = False


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FH6 Dashboard")
        #self.resize(500, 200)
        #self.setWindowOpacity(0.50)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
        )

        self.speed = 0
        self.rpm = 0
        self.rpm_percent = 0
        self.boost = 0

        self.setup_ui()

        self.thread = QThread()
        self.worker = TelemetryWorker()

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.telemetry_ready.connect(self.loop)

        self.thread.start()

    def setup_ui(self):
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.speed_label = QLabel(f"Speed: \n{self.speed} mph")
        self.rpm_label = QLabel(f"RPM: \n{self.rpm}")
        self.boost_label = QLabel(f"Boost: \n{self.boost}")
        self.shift_light = QLabel()

        label_style = """
            font-size: 48px;
            color: white;
            background: transparent;
        """

        self.speed_label.setStyleSheet(label_style)
        self.rpm_label.setStyleSheet(label_style)
        self.boost_label.setStyleSheet(label_style)

        self.shift_light.setFixedSize(150, 150)
        self.shift_light.setStyleSheet("""
            background-color: green;
            border-radius: 25px;
            border: 2px solid black;
        """)

        self.drag_bar = QLabel("Drag")
        self.drag_bar.setFixedHeight(25)
        self.drag_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_bar.setCursor(Qt.CursorShape.SizeAllCursor)

        self.drag_bar.setStyleSheet("""
            color: white;
            background-color: rgba(60, 60, 60, 60);
        """)

        self.drag_bar.mousePressEvent = self.drag_bar_mouse_press

        layout.addWidget(self.drag_bar, 0, 0)

        self.close_button = QPushButton("X")

        self.close_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(60, 60, 60, 60);
            }

            QPushButton:hover {
                background-color: red;
            }
        """)

        self.close_button.clicked.connect(self.close)

        layout.addWidget(self.close_button, 0, 1)

        self.speed_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.rpm_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.boost_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.rpm_label, 1, 0)
        layout.addWidget(
            self.shift_light,
            1,
            1,
            alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(self.speed_label, 2, 0)
        layout.addWidget(self.boost_label, 2, 1)

        #layout.setColumnStretch(0, 1)
        #layout.setColumnStretch(1, 1)
        #layout.setColumnStretch(2, 1)

        self.setLayout(layout)

    def set_shift_light(self):
        if self.rpm_percent < 0.80:
            color = "green"
        elif self.rpm_percent < 0.88:
            color = "yellow"
        elif self.rpm_percent > 0.88:
            color = "red"
        else:
            color = "green"

        self.shift_light.setStyleSheet(f"""
            background-color: {color};
            border-radius: 25px;
            border: 2px solid black;
        """)

    def drag_bar_mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.windowHandle().startSystemMove()
            event.accept()

    def loop(self, t):
        speed_mps = t["Speed"]
        self.speed = speed_mps * 2.23694

        self.rpm = t["CurrentEngineRpm"]
        rpm_max = t["EngineMaxRpm"]
        self.rpm_percent = self.rpm / rpm_max if rpm_max > 0 else 0

        self.boost = t["Boost"]

        #sys.stdout.write("\033[H\033[J")

        #sys.stdout.write(
        #    "FORZA TELEMETRY\n"
        #    "----------------\n"
        #    f"Packet:    {t['_PacketBytes']} bytes\n"
        #    f"Race:      {t['IsRaceOn']}\n"
        #    f"RPM:       {t['CurrentEngineRpm']:.0f}\n"
        #    f"Speed:     {speed_mph:.1f} mph\n"
        #    f"Gear:      {t['Gear']}\n"
        #    f"Throttle:  {t['Accel']}\n"
        #    f"Brake:     {t['Brake']}\n"
        #    f"Steer:     {t['Steer']}\n"
        #    f"Accel X:   {t['AccelerationX']:.3f}\n"
        #    f"Accel Y:   {t['AccelerationY']:.3f}\n"
        #    f"Accel Z:   {t['AccelerationZ']:.3f}\n"
        #    f"Pitch:     {t['Pitch']:.3f}\n"
        #    f"Roll:      {t['Roll']:.3f}\n"
        #    f"Yaw:       {t['Yaw']:.3f}\n"
        #)
        
        self.set_shift_light()
        self.speed_label.setText(f"Speed: \n{self.speed:.1f} mph")
        self.rpm_label.setText(f"RPM: \n{self.rpm:.0f}")
        self.boost_label.setText(f"Boost: \n{self.boost:.0f}")
        #sys.stdout.flush()

    def closeEvent(self, event):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        sock.close()
        event.accept()



def parse_forza_packet(data: bytes) -> dict:
    result = {}
    offset = 0

    for name, fmt in FIELDS:
        size = struct.calcsize("<" + fmt)

        if offset + size > len(data):
            raise ValueError(f"Packet too short at {name}: need {offset + size}, got {len(data)}")

        result[name] = struct.unpack_from("<" + fmt, data, offset)[0]
        offset += size

    # The fields add up to 323 bytes.
    # A 324-byte packet may have 1 trailing byte/padding. Ignore it.
    result["_ParsedBytes"] = offset
    result["_PacketBytes"] = len(data)

    return result


print(f"Listening on {UDP_IP}:{UDP_PORT}")


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()