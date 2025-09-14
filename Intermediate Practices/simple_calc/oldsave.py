from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Calculator")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2f3e46;
            }
            QLabel {
                color: #ffffff;
                font-size: 24px;
                border-radius: 5px;
                padding: 10px;
                background-color: #84a98c;
            }
            QPushButton {
                color: #ffffff;
                font-size: 18px;
                border-radius: 5px;
                padding: 10px;
                background-color: #84a98c;
                min-width: 50px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #354f52;
            }
            QPushButton:pressed {
                background-color: #02befd;
            }
            QPushButton#operator {
                background-color: #52796f;
            }
            QPushButton#operator:hover {
                background-color: #354f52;
            }
            QPushButton#operator:pressed {
                background-color: #02befd;
            }
        """)

        layout = QGridLayout()
        self.label = QLabel("<h1>Enter a Number</h1>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.displayedinput = ''

        self.number_buttons = []
        for i in range(10):
            button = QPushButton(str(i))
            button.clicked.connect(lambda _, num=str(i): self.display(num))
            self.number_buttons.append(button)

        self.buttonadd = QPushButton("+")
        self.buttonsubtract = QPushButton("-")
        self.buttonmultiply = QPushButton("x")
        self.buttondivide = QPushButton("/")
        self.buttonreset = QPushButton("Reset")
        self.button_calculate = QPushButton("=")

        self.buttonadd.setObjectName("operator")
        self.buttonsubtract.setObjectName("operator")
        self.buttonmultiply.setObjectName("operator")
        self.buttondivide.setObjectName("operator")
        self.button_calculate.setObjectName("operator")
        self.buttonreset.setObjectName("operator")

        operators = {
            '+': self.buttonadd,
            '-': self.buttonsubtract,
            'x': self.buttonmultiply,
            '/': self.buttondivide
        }
        for op, button in operators.items():
            button.clicked.connect(lambda _, op=op: self.display(op))

        self.button_calculate.clicked.connect(self.calculate)
        self.buttonreset.clicked.connect(self.reset)

        layout.addWidget(self.label, 0, 0, 1, 4)

        layout.addWidget(self.number_buttons[7], 1, 0)
        layout.addWidget(self.number_buttons[8], 1, 1)
        layout.addWidget(self.number_buttons[9], 1, 2)
        layout.addWidget(self.number_buttons[4], 2, 0)
        layout.addWidget(self.number_buttons[5], 2, 1)
        layout.addWidget(self.number_buttons[6], 2, 2)
        layout.addWidget(self.number_buttons[1], 3, 0)
        layout.addWidget(self.number_buttons[2], 3, 1)
        layout.addWidget(self.number_buttons[3], 3, 2)
        layout.addWidget(self.number_buttons[0], 4, 0, 1, 2)

        layout.addWidget(self.buttonadd, 1, 3)
        layout.addWidget(self.buttonsubtract, 2, 3)
        layout.addWidget(self.buttonmultiply, 3, 3)
        layout.addWidget(self.buttondivide, 4, 3)
        layout.addWidget(self.button_calculate, 4, 2)
        layout.addWidget(self.buttonreset, 5, 0, 1, 4)

        window = QWidget()
        window.setLayout(layout)
        self.setCentralWidget(window)

    def reset(self):
        self.displayedinput = ''
        self.label.setText("<h1>Enter a Number</h1>")

    def display(self, input):
        self.displayedinput += input
        self.label.setText(f"<h1>{self.displayedinput}</h1>")

    def calculate(self):
        try:
            str_input = self.displayedinput
            x = ''
            y = ''
            operator = ''
            second_argument = False
            for char in str_input:
                if not second_argument:
                    if char in '+-x/':
                        operator = char
                        second_argument = True
                    else:
                        x += char
                else:
                    y += char

            print("This is x: ", x)
            print("This is y: ", y)
            print("This is operator: ", operator)
            x = int(x)
            y = int(y)

            if operator == '+':
                z = x+y
            elif operator == '-':
                z = x-y
            elif operator == 'x':
                z = x*y
            elif operator == '/':
                z = x/y

            self.label.setText(f"<h1>{str(z)}</h1>")
        except Exception as e:
            self.label.setText(f"<h1>Error</h1>")


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
