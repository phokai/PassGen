# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 200)
        Form.setMaximumSize(QtCore.QSize(500, 275))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../password-generator-main/icon.ico"),
                       QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Form.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setEnabled(True)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 5, 0, 1, 1)
        self.length = QtWidgets.QLineEdit(self.frame)
        self.length.setInputMethodHints(
            QtCore.Qt.InputMethodHint.ImhFormattedNumbersOnly | QtCore.Qt.InputMethodHint.ImhPreferNumbers)
        self.length.setValidator(QtGui.QIntValidator())
        self.length.setMaxLength(5)
        self.length.setObjectName("length")
        self.gridLayout_2.addWidget(self.length, 5, 1, 1, 1)
        self.password = QtWidgets.QPlainTextEdit(self.frame)
        self.password.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.password.setReadOnly(True)
        self.password.setObjectName("password")
        self.gridLayout_2.addWidget(self.password, 6, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(
            20, 33, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 1, 1, 1)
        self.title = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("title")
        self.gridLayout_2.addWidget(self.title, 4, 1, 1, 1)
        self.info = QtWidgets.QLabel(self.frame)
        self.info.setStyleSheet("color: red;")
        self.info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info.setObjectName("info")
        self.gridLayout_2.addWidget(self.info, 11, 1, 1, 1)
        self.generate = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.generate.setFont(font)
        self.generate.setAutoDefault(True)
        self.generate.setObjectName("generate")
        self.gridLayout_2.addWidget(self.generate, 5, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 12, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PassGen"))
        self.label.setText(_translate("Form", "Password Length:"))
        self.password.setPlainText(_translate("Form", ""))
        self.title.setText(_translate("Form", "Password Generator"))
        self.info.setText(_translate("Form", ""))
        self.generate.setText(_translate("Form", "Generate"))
        self.generate.setShortcut(_translate("Form", "Enter"))
