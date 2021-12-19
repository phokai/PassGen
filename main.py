import sys
import string
import pyperclip
from random import *
from design import *
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
frame = QWidget()
ui = Ui_Form()
ui.setupUi(frame)
frame.show()


def create():
    chars = string.ascii_letters + string.digits + string.punctuation
    length = ui.length.text()
    password = "".join(choice(chars)
                       for _ in range(randint(int(length), int(length))))
    ui.password.setPlainText(password)
    pyperclip.copy(password)
    ui.info.setText("Password copied!")


# __________________________________________________

ui.generate.clicked.connect(create)

sys.exit(app.exec())
