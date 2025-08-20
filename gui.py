import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QDoubleSpinBox, QPushButton, 
                             QFrame, QSizePolicy)
from PyQt6.QtGui import QFont, QPalette, QColor, QPainter, QRegion, QBrush, QMouseEvent
from PyQt6.QtCore import Qt, QByteArray, QPoint
from PyQt6.QtSvgWidgets import QSvgWidget

class BhopAppGUI(QWidget):
    """
    The main GUI for the application.
    Provides controls for the scroller and displays its status.
    """
    def __init__(self):
        super().__init__()
        self.old_pos = QPoint()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Bhop Script Control')
        self.setGeometry(100, 100, 400, 350)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # --- Title Bar ---
        title_bar_layout = QHBoxLayout()
        title_bar_layout.addStretch()

        minimize_button = QPushButton("—")
        minimize_button.setFixedSize(30, 30)
        minimize_button.clicked.connect(self.showMinimized)
        title_bar_layout.addWidget(minimize_button)

        close_button = QPushButton("X")
        close_button.setFixedSize(30, 30)
        close_button.clicked.connect(self.close)
        title_bar_layout.addWidget(close_button)
        
        # --- Main Layout ---
        layout = QVBoxLayout()
        layout.addLayout(title_bar_layout)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)

        # --- Logo Placeholder ---
        logo_widget = QSvgWidget()
        svg_string = '''<?xml version="1.0" encoding="UTF-8"?>
<svg id="_Слой_1" data-name="Слой 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1207.56 936.98">
  <path fill="#FFA500" d="M139.23,658.02c-7.42-35.02-5.58-70.9-21.21-104.46,10.2,1.35,8.35-4.86,8-8.04-.53-4.92-2.74-9.16,2.18-13.63,1.83-1.66,.26-6.68,1-10,.93-4.16,2.99-8.07,3.91-12.23,.77-3.51,.6-7.22,.86-10.98,1.21-.2,4.67-.19,4.84-.93,.48-2.06-.42-4.43-.84-7.08l5.52,.38c-.63-1.92-1.17-3.59-1.88-5.78,2.14,.03,4.12,.07,4.49,.07,6.09-5.67,11.33-10.54,16.7-15.54,5.83,4.88,7.13,4.64,8.61-2.64,16.5,1.49,21.92,15.01,29.56,26.61,15.36-9.4,30.89-19.28,46.78-28.54,19.81-11.55,41-20.13,63.27-25.46,25.04-6,50.17-11.99,75.56-16.04,20.62-3.29,41.2,1.2,61.58,5.35,32.32,6.58,64.8,13.08,98.03,10.07,24.83-2.25,48.07-10.72,71.01-20.26,19.7-8.19,39.61-16,59.86-22.68,12.67-4.18,26.2-5.66,39.21-8.9,13.53-3.37,26.79-7.33,36.64-18.46,7.44-8.41,8.35-18.83,10.46-28.95,4.23-20.32,8.45-40.64,12.27-61.04,.51-2.7-.37-6.77-2.21-8.62-29.25-29.36-52.33-63.21-72.47-99.15-7.66-13.67-15.62-27.54-20.58-42.27-5.74-17.05-8.42-35.13-12.17-52.82-.54-2.53,.42-5.38,.69-8.09,2.95,.45,6.73-.12,8.71,1.51,11.36,9.34,22.7,18.79,33.31,28.96,26.09,25.03,51.75,50.52,77.7,75.7,2.98,2.89,6.72,5,11.57,8.53-.54-11.58-.78-22.08-1.58-32.54-1.73-22.71-4.06-45.38-5.57-68.1-1.33-19.99-2.17-40.03-2.63-60.06-.16-7.1,1.47-14.23,2.28-21.35,.94-.19,1.88-.37,2.82-.56,5.43,7.76,11.08,15.36,16.24,23.29,27.45,42.16,42.92,88.98,53.81,137.65,2.71,12.13,6.51,24.05,10.42,35.86,3.18,9.6,5.49,10.51,15.47,10.02,14.93-.73,29.88-1.5,44.82-1.61,4.56-.03,9.74,1.02,13.62,3.31,23.34,13.78,46.67,27.61,69.39,42.36,12.48,8.1,23.87,17.92,35.52,27.24,5.15,4.12,6.14,10.17,4.21,16.1-4.1,12.59-12.04,23.04-21.69,31.64-15.24,13.58-31.48,26.01-47.1,39.17-5.41,4.55-10.9,9.31-15.03,14.95-2.41,3.29-3.61,8.78-2.83,12.78,1.47,7.51,4.23,14.91,7.42,21.92,6.45,14.15,9.58,28.79,9.2,44.34-.41,16.61,3.53,17.72,20.59,19.45,16.57,1.69,32.69-1.86,49.04-3.4,19.13-1.8,38.61-.93,57.25,5.6,21.83,7.65,44.59,10.12,67.47,12.2,6.53,.59,13.03,2.69,19.3,4.8,4.56,1.53,5.86,5.3,4.3,10.06-4.53,13.85-13.56,24.23-25.21,32.45-19.55,13.8-40.96,19.75-65.21,17.56-35.11-3.17-69.43,2.66-103.47,11.23-7.41,1.86-16.38,1.36-23.7-.97-35.32-11.24-67.26-3.64-98.51,14.02-35.51,20.07-71.35,39.63-107.7,58.13-29.34,14.93-59.04,29.53-89.71,41.32-23.75,9.13-48.99,15.1-74.06,19.88-22.74,4.34-46.11,6.17-69.29,7.15-11.83,.5-23.86-3.17-35.76-5.2-29.41-5.03-58.75-10.47-88.22-15.18-10.54-1.68-21.33-1.94-32.02-2.36-2.11-.08-5.03,1.54-6.37,3.29-21.92,28.8-50.69,48.64-82.88,64.21-15.77,7.63-32.14,7.31-48.67,4.49-27.46-4.68-54.83-9.86-82.27-14.67-2.43-.43-5.38-.29-7.57,.71-15.25,7.03-30.93,13.91-41.64,27.33-5.07,6.36-8.21,14.68-10.73,22.59-5.82,18.28-10.5,36.92-16.08,55.29-7.02,23.11-19.97,42.81-37.03,59.64-9.29,9.17-19.35,17.71-29.83,25.49-7.05,5.24-22.77,2.8-28.47-3.8-2.03-2.35-3.12-7.13-2.24-10.09,4.54-15.26,9.8-30.32,14.93-45.41,4.39-12.91,7.58-26.46,13.75-38.47,9.65-18.79,20.37-37.21,32.51-54.47,9.19-13.05,13.45-26.98,16.58-42.15,5.24-25.43,11.57-50.64,17.87-75.83,1.05-4.19,3.95-8.06,6.55-11.69,3.03-4.22,7.26-5.81,12.46-3.73,7.86,3.14,15.76,6.19,24.26,9.52Z"/>
</svg>'''
        svg_data = QByteArray(svg_string.encode('utf-8'))
        logo_widget.load(svg_data)
        logo_widget.setFixedSize(200, int(200 * 936.98 / 1207.56))
        
        # --- Status Label ---
        self.status_label = QLabel("Status: Stopped")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))

        # --- Settings Layout ---
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(10)

        # Activation Key
        key_layout = QHBoxLayout()
        key_label = QLabel("Activation Key:")
        self.key_input = QLineEdit("space")
        self.key_input.setFixedWidth(120)
        key_layout.addWidget(key_label)
        key_layout.addStretch()
        key_layout.addWidget(self.key_input)

        # Scroll Delay
        delay_layout = QHBoxLayout()
        delay_label = QLabel("Scroll Delay (sec):")
        self.delay_input = QDoubleSpinBox()
        self.delay_input.setFixedWidth(120)
        self.delay_input.setDecimals(4)
        self.delay_input.setSingleStep(0.001)
        self.delay_input.setRange(0.0001, 1.0)
        self.delay_input.setValue(0.001)
        delay_layout.addWidget(delay_label)
        delay_layout.addStretch()
        delay_layout.addWidget(self.delay_input)

        settings_layout.addLayout(key_layout)
        settings_layout.addLayout(delay_layout)

        # --- Buttons Layout ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.start_button = QPushButton("START")
        self.stop_button = QPushButton("STOP")
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # --- Add Widgets to Main Layout ---
        layout.addWidget(logo_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.status_label)
        layout.addStretch(1)
        layout.addLayout(settings_layout)
        layout.addStretch(1)
        layout.addWidget(self.create_separator())
        layout.addLayout(button_layout)

        self.apply_stylesheet()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 255, 255, 240))) # Slightly transparent white
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10) # Less rounded corners
        # super().paintEvent(event) # Don't call super, we are handling the painting

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.old_pos = QPoint()

    def create_separator(self):
        """Creates a styled horizontal line separator."""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setFixedHeight(2)
        return separator

    def apply_stylesheet(self):
        """Applies the orange and white color scheme."""
        self.setStyleSheet("""
            QWidget {
                color: #333333;
                font-family: Arial;
            }
            QLabel {
                font-size: 11pt;
            }
            QLineEdit, QDoubleSpinBox {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                font-size: 11pt;
            }
            QLineEdit:focus, QDoubleSpinBox:focus {
                border: 1px solid #FF8C00; /* Dark Orange */
            }
            QPushButton {
                background-color: #FFA500; /* Orange */
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #FFC04D;
            }
            QPushButton:pressed {
                background-color: #FF8C00; /* Dark Orange */
            }
            QPushButton:disabled {
                background-color: #D3D3D3; /* Light Gray */
                color: #808080;
            }
        """)
        self.status_label.setStyleSheet("color: #FF8C00;") # Initial color for stopped status

    def set_status_running(self):
        """Updates UI to reflect 'Running' state."""
        self.status_label.setText("Status: Running")
        self.status_label.setStyleSheet("color: #008000;") # Green
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.key_input.setEnabled(False)
        self.delay_input.setEnabled(False)

    def set_status_stopped(self):
        """Updates UI to reflect 'Stopped' state."""
        self.status_label.setText("Status: Stopped")
        self.status_label.setStyleSheet("color: #FF8C00;") # Orange
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.key_input.setEnabled(True)
        self.delay_input.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BhopAppGUI()
    window.show()
    sys.exit(app.exec())