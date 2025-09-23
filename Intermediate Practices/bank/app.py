from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

app = QApplication([])

window = QWidget()
window.show()

layout = QVBoxLayout(window)

label = QLabel("<h1>5 plus 5 is...</h1>", parent=window)
button = QPushButton("Calculate!", parent=window)
printer = QPushButton("Click", parent=window)
x = 5
y = 5


def calculate():
    z = x+y
    label.setText(f"<h1>It is equal to {z}! :)</h1>")


def printers():
    print("YOU CLICKED ME!!!!!!")


button.clicked.connect(calculate)
printer.clicked.connect(printers)
layout.addWidget(label)
layout.addWidget(button)
layout.addWidget(printer)
app.exec()
