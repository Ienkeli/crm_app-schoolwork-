from PyQt5 import QtWidgets, QtCore
from ..utils import normalize_phone, format_phone_for_db
from ..db import connection

class AddClientDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить клиента")
        self.setFixedSize(380, 380)
        layout = QtWidgets.QFormLayout()

        self.input_full_name = QtWidgets.QLineEdit()
        self.input_phone = QtWidgets.QLineEdit()
        self.input_phone.setPlaceholderText("10 цифр, например 9991234567")
        self.input_phone.setMaxLength(15)
        self.input_email = QtWidgets.QLineEdit()
        self.input_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.input_date.setCalendarPopup(True)
        self.input_note = QtWidgets.QTextEdit()
        self.input_note.setFixedHeight(80)

        layout.addRow("ФИО:", self.input_full_name)
        layout.addRow("Телефон:", self.input_phone)
        layout.addRow("Email:", self.input_email)
        layout.addRow("Дата обращения:", self.input_date)
        layout.addRow("Примечание:", self.input_note)

        btns = QtWidgets.QHBoxLayout()
        add_btn = QtWidgets.QPushButton("Добавить")
        cancel_btn = QtWidgets.QPushButton("Отмена")
        add_btn.clicked.connect(self.on_add)
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(add_btn)
        btns.addWidget(cancel_btn)

        layout.addRow(btns)
        self.setLayout(layout)

    def on_add(self):
        name = self.input_full_name.text().strip()
        phone_raw = self.input_phone.text().strip()
        if not name:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите ФИО")
            return
        norm = normalize_phone(phone_raw)
        if not norm:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Некорректный телефон")
            return
        self.accept()

    def get_data(self):
        return {
            "full_name": self.input_full_name.text().strip(),
            "phone": self.input_phone.text().strip(),
            "email": self.input_email.text().strip(),
            "request_date": self.input_date.date().toString("yyyy-MM-dd"),
            "note": self.input_note.toPlainText().strip()
        }
