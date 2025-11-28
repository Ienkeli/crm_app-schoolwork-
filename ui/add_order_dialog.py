from PyQt5 import QtWidgets, QtGui, QtCore

class AddOrderDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавление заказа")
        self.setFixedSize(350, 350)

        layout = QtWidgets.QFormLayout()

        self.input_client_id = QtWidgets.QLineEdit()
        self.input_description = QtWidgets.QTextEdit()
        self.input_weight = QtWidgets.QLineEdit()

        self.input_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.input_date.setCalendarPopup(True)

        layout.addRow("ID клиента:", self.input_client_id)
        layout.addRow("Описание:", self.input_description)
        layout.addRow("Вес:", self.input_weight)
        layout.addRow("Дата:", self.input_date)

        btn = QtWidgets.QPushButton("Добавить")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

        self.setLayout(layout)

    def get_data(self):
        return {
            "client_id": self.input_client_id.text(),
            "description": self.input_description.toPlainText(),
            "weight": self.input_weight.text(),
            "date": self.input_date.date().toString("yyyy-MM-dd")
        }
