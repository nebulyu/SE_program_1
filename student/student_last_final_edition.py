import sys
import re

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QScrollArea, QWidget,
    QLabel, QPushButton, QFileDialog
)


class FileViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Rubric")
        self.resize(1200, 800)

        scroll_area = QScrollArea(self)
        self.container = QWidget()
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Tap the bottem to choose the file"))

        self.container.setLayout(self.layout)
        scroll_area.setWidget(self.container)
        scroll_area.setWidgetResizable(True)

        self.setCentralWidget(scroll_area)

        toolbar = self.addToolBar("Files")
        open_button = QPushButton("Open File")
        open_button.setFixedSize(140,45 )
        open_button.clicked.connect(self.load_and_display_file)
        toolbar.addWidget(open_button)

    def load_and_display_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if not filename:
            return

        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()

                    if "TYPE: GRADE" in line:
                        match = re.match(r"TYPE:\s*(GRADE),\s*NOTE:\s*(.+?),\s*VALUE:\s*(\d+)", line)
                        if match:
                            label = QLabel(f"{match.group(1)} | {match.group(2)} | {match.group(3)}")
                            label.setWordWrap(True)
                            self.layout.addWidget(label)

                    elif "TYPE: COMMENT" in line:
                        match = re.match(r"TYPE:\s*(COMMENT),\s*NOTE:\s*(.+?),\s*COMMENT:\s*(.+)", line)
                        if match:
                            label = QLabel(f" {match.group(1)} | {match.group(2)} | {match.group(3)}")
                            label.setWordWrap(True)
                            self.layout.addWidget(label)

                    elif "TYPE:" in line:
                        match = re.match(r"TYPE:\s*(\w+),\s*NOTE:\s*(.+?),\s*TEXT:\s*(.+)", line)
                        if match:
                            label = QLabel(f" {match.group(1)} | {match.group(2)} | {match.group(3)}")
                            label.setWordWrap(True)
                            self.layout.addWidget(label)

                    else:
                        self.layout.addWidget(QLabel(f"Unrecognized line: {line}"))

        except Exception as e:
            self.layout.addWidget(QLabel(f"Error loading file: {e}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wordbig = QFont()
    wordbig.setPointSize(12)
    app.setFont(wordbig)
    viewer = FileViewerApp()
    viewer.show()
    sys.exit(app.exec_())


