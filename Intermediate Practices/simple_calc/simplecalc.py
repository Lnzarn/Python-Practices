from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QPushButton, QGridLayout, QMainWindow)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Calculator")
        self.setFixedSize(300, 400)
        self.setStyleSheet(self.get_stylesheet())
        self.displayedinput = ''

        # Create UI components
        self.label = QLabel("0")
        self.buttons = self.create_buttons()
        self.setup_ui()

    def create_buttons(self):
        buttons = {
            '7': QPushButton("7"),
            '8': QPushButton("8"),
            '9': QPushButton("9"),
            '4': QPushButton("4"),
            '5': QPushButton("5"),
            '6': QPushButton("6"),
            '1': QPushButton("1"),
            '2': QPushButton("2"),
            '3': QPushButton("3"),
            '0': QPushButton("0"),
            '+': QPushButton("+"),
            '-': QPushButton("-"),
            '×': QPushButton("×"),
            '÷': QPushButton("÷"),
            '=': QPushButton("="),
            'C': QPushButton("C"),
            '.': QPushButton(".")
        }

        # Connect buttons
        for key in buttons:
            if key not in ('=', 'C'):
                buttons[key].clicked.connect(lambda _, k=key: self.display(k))

        buttons['='].clicked.connect(self.calculate)
        buttons['C'].clicked.connect(self.reset)

        return buttons

    def setup_ui(self):
        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0, 1, 4)

        # Number buttons
        layout.addWidget(self.buttons['7'], 1, 0)
        layout.addWidget(self.buttons['8'], 1, 1)
        layout.addWidget(self.buttons['9'], 1, 2)
        layout.addWidget(self.buttons['÷'], 1, 3)

        layout.addWidget(self.buttons['4'], 2, 0)
        layout.addWidget(self.buttons['5'], 2, 1)
        layout.addWidget(self.buttons['6'], 2, 2)
        layout.addWidget(self.buttons['×'], 2, 3)

        layout.addWidget(self.buttons['1'], 3, 0)
        layout.addWidget(self.buttons['2'], 3, 1)
        layout.addWidget(self.buttons['3'], 3, 2)
        layout.addWidget(self.buttons['-'], 3, 3)

        layout.addWidget(self.buttons['0'], 4, 0, 1, 2)
        layout.addWidget(self.buttons['.'], 4, 2)
        layout.addWidget(self.buttons['+'], 4, 3)

        # Bottom row
        layout.addWidget(self.buttons['C'], 5, 0, 1, 3)
        layout.addWidget(self.buttons['='], 5, 3)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def reset(self):
        self.displayedinput = ''
        self.label.setText("0")

    def display(self, input):
        self.displayedinput += input
        self.label.setText(self.displayedinput)

    def calculate(self):
        try:
            # Replace × and ÷ with * and / for evaluation
            expression = self.displayedinput.replace(
                '×', '*').replace('÷', '/')
            result = str(eval(expression))
            self.label.setText(result)
            self.displayedinput = result
        except:
            self.label.setText("Error")
            self.displayedinput = ''

    def get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #f0f0f0;
            }
            
            QLabel {
                background-color: white;
                color: black;
                font-size: 24px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                qproperty-alignment: 'AlignRight';
            }
            
            QPushButton {
                background-color: #e0e0e0;
                color: black;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 18px;
                padding: 10px;
            }
            
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
            
            QPushButton[text="+"],
            QPushButton[text="-"],
            QPushButton[text="×"],
            QPushButton[text="÷"] {
                background-color: #f0a050;
                color: white;
            }
            
            QPushButton[text="="] {
                background-color: #50a050;
                color: white;
            }
            
            QPushButton[text="C"] {
                background-color: #a05050;
                color: white;
            }
        """


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
