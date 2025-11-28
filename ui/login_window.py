from PyQt5 import QtWidgets, QtGui, QtCore
from ..auth import check_auth
from ..models import get_full_name
from .database_window import DatabaseWindow

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(360, 220)
        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel("Вход в систему")
        title.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        form = QtWidgets.QFormLayout()
        self.input_id = QtWidgets.QLineEdit()
        self.input_id.setPlaceholderText("ID клиента")
        self.input_id.setValidator(QtGui.QIntValidator())
        form.addRow("Логин (ID):", self.input_id)

        self.input_phone = QtWidgets.QLineEdit()
        self.input_phone.setPlaceholderText("Телефон: 10 цифр, например 9991234567")
        self.input_phone.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_phone.setMaxLength(15)
        form.addRow("Пароль (телефон):", self.input_phone)

        layout.addLayout(form)
        self.status = QtWidgets.QLabel("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.status)

        btn = QtWidgets.QPushButton("Войти")
        btn.clicked.connect(self.on_login)
        layout.addWidget(btn)
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget { background:#121212; color:#eaeaea; }
            QLineEdit { background:#1b1b1b; border:1px solid #333; padding:6px; border-radius:6px; }
            QPushButton { background:#2b2b2b; padding:8px; border-radius:6px; }
            QPushButton:hover { background:#3a3a3a; }
        """)

    def on_login(self):
        user_id = self.input_id.text().strip()
        phone = self.input_phone.text().strip()
        full_name = get_full_name(user_id)

        if not user_id or not phone:
            self.status.setText("Введите логин и пароль")
            self.status.setStyleSheet("color: orange;")
            return

        if check_auth(user_id, phone):
            self.dbwin = DatabaseWindow(user_id, full_name)
            self.dbwin.show()
            self.close()
        else:
            self.status.setText("Неверный логин или пароль")
            self.status.setStyleSheet("color: red;")
