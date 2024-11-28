import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTabWidget, QWidget,
    QLabel, QPushButton, QScrollArea, QFileDialog, QSpinBox, QTextEdit
)
from PyQt5.QtCore import Qt


class GradingApp(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Grading System")
        self.resize(800, 600)

        # Tab widget for pages
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Create pages
        page_data = []
        for entry in self.data:
            page_data.append(entry)
            if entry["TYPE"] == "COMMENT":  # 每遇到一个 COMMENT 类型换页
                self.create_page(page_data)
                page_data = []
        if page_data:  # 处理剩余数据
            self.create_page(page_data)

        # Add Save button to the main window
        save_button = QPushButton("Save to File")
        save_button.setFixedSize(120, 40)
        save_button.clicked.connect(self.save_to_file)
        self.tab_widget.setCornerWidget(save_button, Qt.TopRightCorner)

    def create_page(self, page_data):
        scroll_area = QScrollArea()
        container = QWidget()
        layout = QVBoxLayout()

        for entry in page_data:
            type_ = entry["TYPE"]
            note = entry["NOTE"]
            text = entry["TEXT"]

            if type_ == "TITLE":
                self.handle_title(layout, note, text)
            elif type_ == "INTRODUCTION":
                self.handle_intro(layout, note, text)
            elif type_ == "GRADE":
                self.handle_grade(layout, note)
            elif type_ == "COMMENT":
                self.handle_comment(layout, note)

        container.setLayout(layout)
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)
        self.tab_widget.addTab(scroll_area, f"Page {self.tab_widget.count() + 1}")

    def handle_title(self, layout, note, text):
        note_label = QLabel(f"Title: {note}")
        text_label = QLabel(f"Text: {text}")
        layout.addWidget(note_label)
        layout.addWidget(text_label)

    def handle_intro(self, layout, note, text):
        note_label = QLabel(f"Intro: {note}")
        text_label = QLabel(f"Text: {text}")
        layout.addWidget(note_label)
        layout.addWidget(text_label)

    def handle_grade(self, layout, note):
        note_label = QLabel(f"Grade: {note}")
        spin_box = QSpinBox()
        spin_box.setRange(0, 100)
        spin_box.setSuffix(" / 100d")
        spin_box.setFixedSize(80, 30)  # 宽度 80，高度 30
        layout.addWidget(note_label)
        layout.addWidget(spin_box)

    def handle_comment(self, layout, note):
        note_label = QLabel(f"Note: {note}")
        text_edit = QTextEdit()
        text_edit.setFixedSize(600, 100)  # 设置固定宽度和高度
        layout.addWidget(note_label)
        layout.addWidget(text_edit)

    def save_to_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if not filename:
            return

        with open(filename, "w") as file:
            for entry in self.data:
                type_ = entry["TYPE"]
                note = entry["NOTE"]
                text = entry["TEXT"]

                file.write(f"TYPE: {type_}, NOTE: {note}, TEXT: {text}\n")

        print(f"Data saved to {filename}")

    @staticmethod
    def load_data_from_file():
        """从.tomark文件加载数据并解析"""
        filename, _ = QFileDialog.getOpenFileName(None, "Open .tomark File", "", "Text Files (*.tomark)")
        if not filename:
            return None
        try:
            data = []
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    print(f"Processing line: {line}")  # 打印每一行，检查格式
                    # 使用正则表达式解析文件中的每行
                    match = re.match(r'TYPE:\s*(\w+),\s*NOTE:\s*([^\n,]+),\s*TEXT:\s*(.*)', line.strip())
                    if match:
                        data.append({
                            'TYPE': match.group(1),
                            'NOTE': match.group(2),
                            'TEXT': match.group(3)
                        })
                    else:
                        print(f"Line did not match expected format: {line}")  # 输出未匹配的行

            # 调试输出：打印加载的数据
            print("Loaded data:", data)
            return data
        except Exception as e:
            print(f"Error loading file: {e}")
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 从文件加载数据
    data = GradingApp.load_data_from_file()

    if data is not None:
        window = GradingApp(data)
        window.show()
        sys.exit(app.exec_())