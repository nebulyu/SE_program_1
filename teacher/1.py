import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QTextEdit,
    QPushButton, QWidget, QFileDialog
)

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Homework Grading Tool")
        self.data = data
        self.results = {}  # 用于存储用户输入
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        for entry in self.data:
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

        save_button = QPushButton("Save to File")
        save_button.clicked.connect(self.save_to_file)
        layout.addWidget(save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_title(self, layout, note, text):
        layout.addWidget(QLabel(f"NOTE: {note}"))
        layout.addWidget(QLabel(f"TEXT: {text}"))

    def handle_intro(self, layout, note, text):
        layout.addWidget(QLabel(f"NOTE: {note}"))
        layout.addWidget(QLabel(f"TEXT: {text}"))

    def handle_grade(self, layout, note):
        layout.addWidget(QLabel(f"NOTE: {note}"))
        spin_box = QSpinBox()
        spin_box.setRange(0, 100)
        layout.addWidget(spin_box)
        self.results[note] = spin_box

    def handle_comment(self, layout, note):
        layout.addWidget(QLabel(f"NOTE: {note}"))
        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        self.results[note] = text_edit

    def save_to_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if not filename:
            return

        with open(filename, "w") as file:
            for entry in self.data:
                type_ = entry["TYPE"]
                note = entry["NOTE"]
                text = entry.get("TEXT", "")

                if type_ in ["TITLE", "INTRODUCTION"]:
                    file.write(f"TYPE: {type_}, NOTE: {note}, TEXT: {text}\n")
                elif type_ == "GRADE":
                    score = self.results[note].value()
                    file.write(f"TYPE: {type_}, NOTE: {note}, TEXT: {text}, SCORE: {score}\n")
                elif type_ == "COMMENT":
                    comment = self.results[note].toPlainText()
                    file.write(f"TYPE: {type_}, NOTE: {note}, TEXT: {text}, COMMENT: {comment}\n")

        print(f"File saved: {filename}")


if __name__ == "__main__":
    data = [
        {"TYPE": "TITLE", "NOTE": "Homework Grading", "TEXT": "Grades"},
        {"TYPE": "TITLE", "NOTE": "Section 1", "TEXT": "Grades for Section 1"},
        {"TYPE": "TITLE", "NOTE": "clarity", "TEXT": "clarity for Section 1"},
        {"TYPE": "INTRODUCTION", "NOTE": "Evaluate clarity", "TEXT": "The clarity of homework"},
        {"TYPE": "GRADE", "NOTE": "Grades clarity", "TEXT": "Your score of clarity"},
        {"TYPE": "COMMENT", "NOTE": "Comment clarity", "TEXT": "Marker's comment on clarity"}


    ]

    app = QApplication(sys.argv)
    window = MainWindow(data)
    window.show()
    sys.exit(app.exec_())
